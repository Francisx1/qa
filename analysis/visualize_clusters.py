from pathlib import Path
import pickle
import json

import numpy as np
import matplotlib.pyplot as plt

# Optional: UMAP (recommended). If not installed, fallback to TSNE.
try:
    import umap
    HAS_UMAP = True
except Exception:
    HAS_UMAP = False

from sklearn.manifold import TSNE


def load_cluster_data(cluster_dir: Path):
    pkl_path = cluster_dir / "cluster_data.pkl"
    if not pkl_path.exists():
        raise FileNotFoundError(f"Not found: {pkl_path}. Run `python example.py` to generate it.")

    with open(pkl_path, "rb") as f:
        data = pickle.load(f)

    labels = np.asarray(data["labels"])
    embeddings = np.asarray(data["embeddings"])
    return embeddings, labels


def load_cluster_name_map(cluster_dir: Path):
    """
    Load cluster id -> human-friendly name from clusters.json
    Returns {} if file missing.
    """
    json_path = cluster_dir / "clusters.json"
    if not json_path.exists():
        return {}

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    name_map = {}
    for c in data.get("clusters", []):
        try:
            cid = int(c.get("id"))
        except Exception:
            continue
        name_map[cid] = c.get("name", f"cluster {cid}")
    return name_map


def reduce_to_2d(X: np.ndarray):
    if HAS_UMAP:
        reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, random_state=42)
        Z = reducer.fit_transform(X)
        method = "UMAP"
    else:
        reducer = TSNE(n_components=2, perplexity=30, random_state=42, init="pca")
        Z = reducer.fit_transform(X)
        method = "t-SNE"
    return Z, method


def main():
    root = Path(__file__).resolve().parents[1]      # qa_github/
    cluster_dir = root / "data" / "clusters"

    X, labels = load_cluster_data(cluster_dir)
    name_map = load_cluster_name_map(cluster_dir)

    Z, method = reduce_to_2d(X)

    # Plot
    plt.figure(figsize=(9, 7))

    # noise first
    noise = labels == -1
    if noise.any():
        plt.scatter(Z[noise, 0], Z[noise, 1], s=10, alpha=0.30, label="noise (-1)")

    # clusters
    for cid in np.unique(labels):
        if cid == -1:
            continue
        idx = labels == cid
        plt.scatter(Z[idx, 0], Z[idx, 1], s=14, alpha=0.70, label=f"cluster {cid}")

        # centroid label: "id: name"
        cx, cy = Z[idx, 0].mean(), Z[idx, 1].mean()
        cname = name_map.get(int(cid), f"cluster {cid}")
        label = f"{cid}: {cname}"

        # 把 label 放到簇下方：根据图的y轴范围算一个“相对偏移”，不同数据尺度也稳
        y_span = float(Z[:, 1].max() - Z[:, 1].min() + 1e-9)
        dy = 0.04 * y_span   # 4% 的纵向跨度，你想更远就 0.06/0.08
        label_x = cx
        label_y = cy - dy

        plt.text(
            label_x, label_y, label,
            fontsize=8, weight="bold",
            ha="center", va="top",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="white", alpha=0.75, linewidth=0),
            zorder=5)


    plt.title(f"{method} visualization of HDBSCAN clusters")
    plt.tight_layout()

    # If legend gets too crowded, you can comment this out
    plt.legend(markerscale=1.5, fontsize=8, ncol=2)

    out_png = cluster_dir / f"cluster_{method.lower()}.png"
    plt.savefig(out_png, dpi=220)
    print(f"Saved plot to: {out_png}")


if __name__ == "__main__":
    main()