import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA


# ==========================================
# BugCluster - PCA Cluster Visualization
# ==========================================

DATA_PATH = "../data/processed/clustered_bugs.csv"
OUTPUT_PATH = "../data/processed/cluster_visualization.png"


# ==========================================
# 1. LOAD DATA
# ==========================================

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully!")
print("Number of bugs:", len(df))


# ==========================================
# 2. TF-IDF FEATURE EXTRACTION
# ==========================================

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=1000,
    ngram_range=(1, 2)
)

tfidf_matrix = vectorizer.fit_transform(
    df["bug_text"]
)

print("TF-IDF shape:", tfidf_matrix.shape)


# ==========================================
# 3. PCA
# ==========================================

pca = PCA(
    n_components=2,
    random_state=42
)

pca_result = pca.fit_transform(
    tfidf_matrix.toarray()
)

df["pca_x"] = pca_result[:, 0]
df["pca_y"] = pca_result[:, 1]


print("\n========== PCA RESULTS ==========")

print(
    "Explained variance ratio:"
)

print(
    pca.explained_variance_ratio_
)

print(
    "Total explained variance:",
    f"{pca.explained_variance_ratio_.sum():.4f}"
)


# ==========================================
# 4. CREATE VISUALIZATION
# ==========================================

plt.figure(
    figsize=(12, 8)
)

clusters = sorted(
    df["cluster"].unique()
)

colors = plt.cm.tab10(
    range(len(clusters))
)


for cluster, color in zip(
    clusters,
    colors
):

    cluster_data = df[
        df["cluster"] == cluster
    ]

    plt.scatter(
        cluster_data["pca_x"],
        cluster_data["pca_y"],
        label=f"Cluster {cluster}",
        color=color,
        s=70,
        alpha=0.75
    )


# ==========================================
# 5. LABEL BUGS
# ==========================================

for _, row in df.iterrows():

    plt.annotate(
        row["bug_id"],
        (
            row["pca_x"],
            row["pca_y"]
        ),
        fontsize=7,
        alpha=0.7
    )


# ==========================================
# 6. GRAPH FORMATTING
# ==========================================

plt.title(
    "BugCluster - PCA Visualization of Bug Clusters",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel(
    "Principal Component 1"
)

plt.ylabel(
    "Principal Component 2"
)

plt.legend(
    title="Bug Clusters",
    bbox_to_anchor=(1.05, 1),
    loc="upper left"
)

plt.grid(
    True,
    linestyle="--",
    alpha=0.3
)

plt.tight_layout()


# ==========================================
# 7. SAVE GRAPH
# ==========================================

plt.savefig(
    OUTPUT_PATH,
    dpi=300,
    bbox_inches="tight"
)

plt.show()


print("\n===================================")
print("PCA visualization created!")
print("File:", OUTPUT_PATH)
print("===================================")
