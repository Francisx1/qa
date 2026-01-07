"""
Auto-clustering for knowledge organization
Automatically discovers and groups related documents
"""
import numpy as np
from typing import List, Dict, Any, Optional
from collections import Counter
from pathlib import Path
import pickle
import json
import hashlib
import re

try:
    from sklearn.cluster import KMeans, AgglomerativeClustering
    from sklearn.preprocessing import normalize
    from sklearn.feature_extraction.text import TfidfVectorizer
    import hdbscan
    from sentence_transformers import SentenceTransformer
except ImportError:
    KMeans = None
    AgglomerativeClustering = None
    normalize = None
    TfidfVectorizer = None
    hdbscan = None
    SentenceTransformer = None


class AutoClusterer:
    """
    Automatically clusters documents based on semantic similarity
    Helps organize scattered notes into meaningful categories
    """

    def __init__(self, config):
        self.config = config
        self.algorithm = config.get('clustering.algorithm', 'hdbscan')
        self.min_cluster_size = config.get('clustering.min_cluster_size', 3)
        self.max_clusters = config.get('clustering.max_clusters', 20)

        # Tunables (safe defaults)
        self.min_samples = config.get('clustering.min_samples', None)
        self.metric = config.get('clustering.metric', 'cosine')
        self.representation_max_chars = config.get('clustering.representation_max_chars', 1000)

        self.enable_dedup = config.get('clustering.dedup', True)
        self.enable_text_clean = config.get('clustering.text_clean', True)
        self.enable_tfidf_naming = config.get('clustering.tfidf_naming', True)

        # Initialize embedding model
        if SentenceTransformer:
            model_name = config.get('search.semantic.model',
                                    'sentence-transformers/all-MiniLM-L6-v2')
            self.model = SentenceTransformer(model_name)
        else:
            self.model = None

        self.documents: List[Dict[str, Any]] = []
        self.embeddings: Optional[np.ndarray] = None
        self.clusters: Optional[List[Dict[str, Any]]] = None
        self.cluster_labels: Optional[np.ndarray] = None

        # For naming
        self._embed_texts: List[str] = []   # representation for embedding
        self._name_texts: List[str] = []    # representation for TF-IDF naming (exclude tag_ tokens)

    # -------------------------
    # Main API
    # -------------------------
    def fit(self, documents: List[Dict[str, Any]], embeddings: Optional[np.ndarray] = None):
        if not documents:
            return {'clusters': [], 'labels': [], 'num_clusters': 0}

        docs = list(documents)

        # 1) Strong dedupe to handle re-index + timestamp differences
        if self.enable_dedup:
            docs = self._dedupe_documents(docs)

        self.documents = docs

        # 2) Build texts for embedding & naming
        self._embed_texts = [self._build_embedding_text(doc) for doc in self.documents]
        self._name_texts = [self._build_naming_text(doc) for doc in self.documents]

        # 3) Embeddings
        if embeddings is None:
            if not self.model:
                raise ValueError("SentenceTransformer model not available")
            print(f"Generating embeddings for {len(self.documents)} documents...")
            self.embeddings = self.model.encode(self._embed_texts, show_progress_bar=True)
        else:
            self.embeddings = embeddings

        # 4) Normalize
        if normalize is None:
            raise ImportError("scikit-learn not installed (normalize unavailable)")
        self.embeddings = normalize(self.embeddings)

        # 5) Clustering
        print(f"Clustering with {self.algorithm}...")
        if self.algorithm == 'kmeans':
            self.cluster_labels = self._kmeans_cluster()
        elif self.algorithm == 'hierarchical':
            self.cluster_labels = self._hierarchical_cluster()
        elif self.algorithm == 'hdbscan':
            self.cluster_labels = self._hdbscan_cluster()
        else:
            raise ValueError(f"Unknown clustering algorithm: {self.algorithm}")

        # 6) Organize results
        self.clusters = self._organize_clusters()

        # 7) Name clusters
        if self.config.get('clustering.auto_naming', True):
            self._name_clusters()

        return {
            'clusters': self.clusters,
            'labels': self.cluster_labels,
            'num_clusters': len(self.clusters)
        }

    # -------------------------
    # Clustering algorithms
    # -------------------------
    def _effective_min_cluster_size(self) -> int:
        n = len(self.documents)
        base = int(self.min_cluster_size) if self.min_cluster_size else 3
        # gentle bump to avoid micro clusters / too much noise
        if n >= 120:
            return max(base, 8)
        if n >= 60:
            return max(base, 5)
        return base

    def _effective_n_clusters(self) -> int:
        n = len(self.documents)
        min_cs = self._effective_min_cluster_size()
        n_clusters = min(self.max_clusters, max(2, n // max(1, min_cs)))
        return max(2, n_clusters)

    def _kmeans_cluster(self) -> np.ndarray:
        if KMeans is None:
            raise ImportError("scikit-learn not installed")
        n_clusters = self._effective_n_clusters()
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        return kmeans.fit_predict(self.embeddings)

    def _hierarchical_cluster(self) -> np.ndarray:
        if AgglomerativeClustering is None:
            raise ImportError("scikit-learn not installed")
        n_clusters = self._effective_n_clusters()
        clustering = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
        return clustering.fit_predict(self.embeddings)

    def _hdbscan_cluster(self) -> np.ndarray:
        if hdbscan is None:
            raise ImportError("hdbscan not installed")

        min_cluster_size = self._effective_min_cluster_size()
        min_samples = self.min_samples
        if min_samples is None:
            min_samples = max(3, min_cluster_size // 2)

        metric = self.metric or 'cosine'

        try:
            clusterer = hdbscan.HDBSCAN(
                min_cluster_size=min_cluster_size,
                min_samples=min_samples,
                metric=metric
            )
            return clusterer.fit_predict(self.embeddings)
        except Exception:
            # fallback for older/stricter installs
            clusterer = hdbscan.HDBSCAN(
                min_cluster_size=min_cluster_size,
                min_samples=min_samples,
                metric='euclidean'
            )
            return clusterer.fit_predict(self.embeddings)

    # -------------------------
    # Organize clusters
    # -------------------------
    def _organize_clusters(self) -> List[Dict[str, Any]]:
        unique_labels = set(self.cluster_labels.tolist() if hasattr(self.cluster_labels, "tolist") else list(self.cluster_labels))
        clusters: List[Dict[str, Any]] = []

        for label in sorted(unique_labels):
            label = int(label)
            cluster_name = "Uncategorized" if label == -1 else f"Cluster {label}"

            doc_indices = np.where(self.cluster_labels == label)[0]
            cluster_docs = [self.documents[idx] for idx in doc_indices]

            all_tags = []
            for doc in cluster_docs:
                meta = doc.get('metadata', {}) or {}
                tags = meta.get('tags', []) or []
                all_tags.extend(tags)

            common_tags = [tag for tag, _ in Counter(all_tags).most_common(5)]

            clusters.append({
                'id': label,
                'name': cluster_name,
                'size': len(cluster_docs),
                'documents': cluster_docs,
                'doc_indices': doc_indices.tolist(),
                'common_tags': common_tags,
                'keywords': []
            })

        # sort: big first, put Uncategorized last
        clusters.sort(key=lambda c: (c['id'] == -1, -c['size']))
        return clusters

    # -------------------------
    # Naming strategy
    # -------------------------
    def _name_clusters(self):
        """
        Naming policy (as you requested):
        - TF-IDF keywords drive naming (primary)
        - tags are secondary (display only / fallback)
        - Uncategorized keeps its name, but still gets keywords (so it looks informative)
        """
        # Ensure Uncategorized name is stable
        for c in self.clusters:
            if c['id'] == -1:
                c['name'] = "Uncategorized"

        # Prefer TF-IDF if available
        if self.enable_tfidf_naming and TfidfVectorizer is not None and self._name_texts:
            try:
                self._name_clusters_tfidf()
                return
            except Exception:
                pass

        # Fallback to a safer counter method
        self._name_clusters_counter_fallback()

    def _name_clusters_tfidf(self):
        # Add a few domain-generic stopwords to avoid "documents/based/cluster"
        extra_stop = {
            'document', 'documents', 'based', 'cluster', 'clustering', 'data', 'text',
            'note', 'notes', 'example', 'examples', 'introduction', 'overview'
        }

        vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=20000,
            ngram_range=(1, 2),
            min_df=2
        )
        X = vectorizer.fit_transform(self._name_texts)
        vocab = np.array(vectorizer.get_feature_names_out())

        for cluster in self.clusters:
            idxs = cluster.get('doc_indices', [])
            if not idxs:
                continue

            mean_vec = X[idxs].mean(axis=0)
            mean_vec = np.asarray(mean_vec).ravel()

            top = mean_vec.argsort()[-20:][::-1]
            keywords = []
            for i in top:
                if mean_vec[i] <= 0:
                    break
                kw = vocab[i]
                # filter out extra stopwords + any leftover tag_ token
                if kw.startswith("tag_"):
                    continue
                if kw in extra_stop:
                    continue
                keywords.append(kw)
                if len(keywords) >= 10:
                    break

            cluster['keywords'] = keywords

            # Naming: keyword-first, tag as fallback
            if cluster['id'] == -1:
                # Keep name "Uncategorized" but allow keywords for display
                continue

            if keywords:
                # Make name short & readable: top1 • top2
                if len(keywords) >= 2:
                    cluster['name'] = f"{keywords[0].title()} • {keywords[1]}"
                else:
                    cluster['name'] = f"{keywords[0].title()} Topics"
            else:
                tags = cluster.get('common_tags', []) or []
                if tags:
                    cluster['name'] = " / ".join([t for t in tags[:2]])
                else:
                    cluster['name'] = f"Cluster {cluster['id']}"

    def _name_clusters_counter_fallback(self):
        stop_words = {
            'this', 'that', 'with', 'from', 'have', 'been', 'will', 'about', 'which', 'their',
            'would', 'there', 'these', 'those', 'into', 'over', 'under', 'between', 'within',
            'also', 'than', 'then', 'when', 'where', 'what', 'why', 'how',
            'document', 'documents', 'based', 'cluster', 'clustering', 'data', 'text'
        }

        for cluster in self.clusters:
            all_text = ' '.join([doc.get('content', '') or '' for doc in cluster['documents']])
            words = re.findall(r'\b[a-z]{4,}\b', all_text.lower())
            words = [w for w in words if w not in stop_words]
            keywords = [w for w, _ in Counter(words).most_common(10)]
            cluster['keywords'] = keywords

            if cluster['id'] == -1:
                cluster['name'] = "Uncategorized"
                continue

            if keywords:
                cluster['name'] = f"{keywords[0].title()} Topics"
            else:
                tags = cluster.get('common_tags', []) or []
                cluster['name'] = " / ".join(tags[:2]) if tags else f"Cluster {cluster['id']}"

    # -------------------------
    # Text building & cleaning
    # -------------------------
    def _clean_markdown(self, text: str) -> str:
        if not text:
            return ""
        text = re.sub(r"^---.*?---\s*", "", text, flags=re.S)        # frontmatter
        text = re.sub(r"```.*?```", " ", text, flags=re.S)           # fenced code
        text = re.sub(r"`[^`]+`", " ", text)                         # inline code
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)         # md links
        text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)              # wiki links
        text = re.sub(r"^\s*#{1,6}\s*", "", text, flags=re.M)        # headings
        text = re.sub(r"^\s*[-*+]\s*", "", text, flags=re.M)         # bullets
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _strip_timestamps(self, text: str) -> str:
        """
        Remove timestamp-like tokens so repeated indexing with different timestamps
        won't break content-hash dedupe.
        """
        if not text:
            return ""

        # ISO dates: 2026-01-07, 2026/01/07
        text = re.sub(r"\b20\d{2}[-/]\d{1,2}[-/]\d{1,2}\b", " ", text)

        # Times: 12:34, 12:34:56
        text = re.sub(r"\b\d{1,2}:\d{2}(:\d{2})?\b", " ", text)

        # Full timestamp: 2026-01-07T12:34:56 or 2026-01-07 12:34:56
        text = re.sub(r"\b20\d{2}[-/]\d{1,2}[-/]\d{1,2}[T\s]\d{1,2}:\d{2}(:\d{2})?\b", " ", text)

        # Unix-like long numbers (10-13 digits)
        text = re.sub(r"\b\d{10,13}\b", " ", text)

        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _normalize_title(self, title: str) -> str:
        """
        Normalize titles like:
        'Agents - Function Calling (9)' -> 'Agents - Function Calling'
        """
        if not title:
            return ""
        t = title.strip()
        t = re.sub(r"\s*\(\d+\)\s*$", "", t)   # remove trailing "(9)"
        t = re.sub(r"\s*-\s*\d+\s*$", "", t)  # remove trailing "- 9"
        t = re.sub(r"\s+", " ", t).strip()
        return t.lower()

    def _build_embedding_text(self, doc: Dict[str, Any]) -> str:
        meta = doc.get('metadata', {}) or {}
        title = (meta.get('title', '') or '').strip()
        tags = meta.get('tags', []) or []
        tags = [t.strip() for t in tags if isinstance(t, str) and t.strip()]

        content = (doc.get('content', '') or '')
        if self.enable_text_clean:
            content = self._clean_markdown(content)

        content = content[: int(self.representation_max_chars)]
        tags_str = " ".join([f"tag_{t}" for t in tags])

        # Title-weighting helps stability
        rep = f"{title}. {title}. {tags_str}. {content}".strip()
        return rep if rep else "empty"

    def _build_naming_text(self, doc: Dict[str, Any]) -> str:
        """
        For TF-IDF naming we should NOT inject tag_ tokens,
        otherwise keywords get polluted by tags.
        """
        meta = doc.get('metadata', {}) or {}
        title = (meta.get('title', '') or '').strip()

        content = (doc.get('content', '') or '')
        if self.enable_text_clean:
            content = self._clean_markdown(content)

        content = content[: int(self.representation_max_chars)]
        rep = f"{title}. {content}".strip()
        return rep if rep else "empty"

    # -------------------------
    # Dedupe
    # -------------------------
    def _dedupe_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Strong dedupe rules to handle:
        - repeated indexing producing multiple copies
        - timestamp differences in content
        - titles with (1)(2)(9)

        Strategy:
        - key1: normalized path (if present)
        - key2: canonical content hash (markdown-clean + strip timestamps)
        - key3: normalized title + canonical prefix hash (helps when path missing)
        """
        seen_paths = set()
        seen_canon_hash = set()
        seen_title_prefix = set()
        uniq = []

        for d in documents:
            meta = d.get('metadata', {}) or {}
            path = (meta.get('path', '') or '').strip().lower()
            title = (meta.get('title', '') or '')

            raw = (d.get('content', '') or '').strip()
            cleaned = self._clean_markdown(raw) if self.enable_text_clean else raw
            canon = self._strip_timestamps(cleaned)

            # Canonical hash
            canon_hash = hashlib.md5(canon.encode('utf-8')).hexdigest() if canon else None

            # Title+prefix hash (for cases where only tiny timestamp differs)
            norm_title = self._normalize_title(title)
            canon_prefix = canon[:800]  # enough to be stable, not too large
            title_prefix_key = (norm_title, hashlib.md5(canon_prefix.encode('utf-8')).hexdigest() if canon_prefix else "")

            # path-based dedupe
            if path:
                if path in seen_paths:
                    continue
                seen_paths.add(path)

            # canonical content dedupe
            if canon_hash:
                if canon_hash in seen_canon_hash:
                    continue
                seen_canon_hash.add(canon_hash)

            # title+prefix dedupe (catches "same note, different timestamp, different file path")
            if norm_title and title_prefix_key[1]:
                if title_prefix_key in seen_title_prefix:
                    continue
                seen_title_prefix.add(title_prefix_key)

            uniq.append(d)

        return uniq

    # -------------------------
    # Others (unchanged behaviors)
    # -------------------------
    def get_cluster_summary(self) -> str:
        if not self.clusters:
            return "No clusters found"

        lines = [f"Total Clusters: {len(self.clusters)}\n"]
        for cluster in self.clusters:
            lines.append(f"\n{cluster['name']} (ID: {cluster['id']})")
            lines.append(f"  Size: {cluster['size']} documents")
            if cluster.get('common_tags'):
                lines.append(f"  Tags: {', '.join(cluster['common_tags'][:3])}")
            if cluster.get('keywords'):
                lines.append(f"  Keywords: {', '.join(cluster['keywords'][:5])}")
            sample_docs = cluster.get('documents', [])[:3]
            if sample_docs:
                lines.append("  Sample documents:")
                for doc in sample_docs:
                    title = (doc.get('metadata', {}) or {}).get('title', 'Untitled')
                    lines.append(f"    - {title}")
        return '\n'.join(lines)

    def find_similar_clusters(self, doc_index: int, top_k: int = 3) -> List[Dict[str, Any]]:
        if self.embeddings is None or not self.clusters:
            return []

        doc_embedding = self.embeddings[doc_index]
        similarities = []

        for cluster in self.clusters:
            if cluster['id'] == -1:
                continue
            cluster_embeddings = self.embeddings[cluster['doc_indices']]
            cluster_center = np.mean(cluster_embeddings, axis=0)
            similarity = float(np.dot(doc_embedding, cluster_center))
            similarities.append({'cluster': cluster, 'similarity': similarity})

        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        return similarities[:top_k]

    def save(self, path: str):
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)

        cluster_data = []
        for cluster in (self.clusters or []):
            cluster_data.append({
                'id': cluster['id'],
                'name': cluster['name'],
                'size': cluster['size'],
                'doc_indices': cluster['doc_indices'],
                'common_tags': cluster.get('common_tags', []),
                'keywords': cluster.get('keywords', [])
            })

        with open(path / "clusters.json", 'w', encoding='utf-8') as f:
            json.dump({
                'clusters': cluster_data,
                'algorithm': self.algorithm,
                'num_documents': len(self.documents)
            }, f, indent=2)

        with open(path / "cluster_data.pkl", 'wb') as f:
            pickle.dump({
                'labels': self.cluster_labels,
                'embeddings': self.embeddings
            }, f)

    def load(self, path: str):
        path = Path(path)

        with open(path / "clusters.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.clusters = data['clusters']

        with open(path / "cluster_data.pkl", 'rb') as f:
            data = pickle.load(f)
            self.cluster_labels = data['labels']
            self.embeddings = data['embeddings']
