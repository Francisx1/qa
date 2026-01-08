from pathlib import Path
import pickle
from collections import Counter

import numpy as np
from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score,
    calinski_harabasz_score,
)


def load_cluster_data(cluster_dir: Path):
    pkl_path = cluster_dir / "cluster_data.pkl"
    if not pkl_path.exists():
        raise FileNotFoundError(f"Not found: {pkl_path}. Run your clustering first to generate it.")

    with open(pkl_path, "rb") as f:
        data = pickle.load(f)

    labels = np.asarray(data["labels"])
    embeddings = np.asarray(data["embeddings"])
    return embeddings, labels


def safe_metrics(X: np.ndarray, y: np.ndarray):
    """
    Compute common unsupervised clustering metrics safely.
    Assumes y contains NO noise label (-1) and has >= 2 clusters.
    """
    metrics = {}

    # Silhouette: higher is better
    metrics["silhouette_cosine"] = float(silhouette_score(X, y, metric="cosine"))
    metrics["silhouette_euclidean"] = float(silhouette_score(X, y, metric="euclidean"))

    # Davies-Bouldin: lower is better (uses euclidean geometry)
    metrics["davies_bouldin"] = float(davies_bouldin_score(X, y))

    # Calinski-Harabasz: higher is better (uses euclidean geometry)
    metrics["calinski_harabasz"] = float(calinski_harabasz_score(X, y))

    return metrics


def main():
    root = Path(__file__).resolve().parents[1]  # project root
    cluster_dir = root / "data" / "clusters"

    X, labels = load_cluster_data(cluster_dir)

    total = len(labels)
    noise_mask = labels == -1
    non_noise_mask = ~noise_mask

    n_noise = int(noise_mask.sum())
    n_non_noise = int(non_noise_mask.sum())
    uniq = np.unique(labels[non_noise_mask])
    n_clusters = len(uniq)

    print("=== Cluster Evaluation (HDBSCAN) ===")
    print(f"Total points: {total}")
    print(f"Noise points (-1): {n_noise} ({n_noise/total:.1%})")
    print(f"Non-noise points: {n_non_noise}")
    print(f"Num clusters (excluding noise): {n_clusters}")

    # cluster sizes (excluding noise)
    counts = Counter(labels[non_noise_mask].tolist())
    top_sizes = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]
    print("\nTop cluster sizes (id: size):")
    for cid, sz in top_sizes:
        print(f"  {cid}: {sz}")

    # metrics
    metrics = None
    if n_clusters >= 2 and n_non_noise >= 3:
        X_nn = X[non_noise_mask]
        y_nn = labels[non_noise_mask]
        metrics = safe_metrics(X_nn, y_nn)

        print("\nQuality metrics (excluding noise):")
        print(f"  Silhouette (cosine)   : {metrics['silhouette_cosine']:.4f}  (higher better)")
        print(f"  Silhouette (euclidean): {metrics['silhouette_euclidean']:.4f}  (higher better)")
        print(f"  Davies-Bouldin        : {metrics['davies_bouldin']:.4f}  (lower better)")
        print(f"  Calinski-Harabasz     : {metrics['calinski_harabasz']:.2f}  (higher better)")
    else:
        print("\nQuality metrics: N/A (need >=2 clusters after removing noise).")

    # save txt summary
    out_txt = cluster_dir / "evaluation_summary.txt"
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("=== Cluster Evaluation (HDBSCAN) ===\n")
        f.write(f"Total points: {total}\n")
        f.write(f"Noise points (-1): {n_noise} ({n_noise/total:.1%})\n")
        f.write(f"Non-noise points: {n_non_noise}\n")
        f.write(f"Num clusters (excluding noise): {n_clusters}\n")

        f.write("\nTop cluster sizes (id: size):\n")
        for cid, sz in top_sizes:
            f.write(f"  {cid}: {sz}\n")

        if metrics is not None:
            f.write("\nQuality metrics (excluding noise):\n")
            f.write(f"  Silhouette (cosine)   : {metrics['silhouette_cosine']:.4f}  (higher better)\n")
            f.write(f"  Silhouette (euclidean): {metrics['silhouette_euclidean']:.4f}  (higher better)\n")
            f.write(f"  Davies-Bouldin        : {metrics['davies_bouldin']:.4f}  (lower better)\n")
            f.write(f"  Calinski-Harabasz     : {metrics['calinski_harabasz']:.2f}  (higher better)\n")
        else:
            f.write("\nQuality metrics: N/A (need >=2 clusters after removing noise).\n")

        # Optional: add a short interpretation block for the report
        f.write("\nInterpretation tips:\n")
        f.write("- Noise% shows how many points are considered outliers by HDBSCAN.\n")
        f.write("- Silhouette near 1 means well-separated clusters; near 0 means overlapping.\n")
        f.write("- Lower DBI indicates tighter, better-separated clusters.\n")
        f.write("- Higher CH indicates better defined clusters (but grows with sample size).\n")

    print(f"\nSaved summary to: {out_txt}")


if __name__ == "__main__":
    main()