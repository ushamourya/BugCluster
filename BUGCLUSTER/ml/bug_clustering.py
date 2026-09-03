import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


# ==========================================
# BugCluster - K-Means Clustering
# ==========================================

DATA_PATH = "../data/processed/clean_bugs.csv"
OUTPUT_PATH = "../data/processed/clustered_bugs.csv"


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

print("\nTF-IDF matrix shape:")
print(tfidf_matrix.shape)


feature_names = vectorizer.get_feature_names_out()

print("\nNumber of TF-IDF features:")
print(len(feature_names))


# ==========================================
# 3. FIND BEST NUMBER OF CLUSTERS
# ==========================================

print("\n========== SILHOUETTE SCORES ==========")

scores = {}

# Test reasonable cluster sizes
max_k = min(10, len(df) - 1)

for k in range(2, max_k + 1):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=20
    )

    labels = model.fit_predict(
        tfidf_matrix
    )

    score = silhouette_score(
        tfidf_matrix,
        labels
    )

    scores[k] = score

    print(
        f"K = {k}  |  "
        f"Silhouette Score = {score:.4f}"
    )


# ==========================================
# 4. SELECT BEST K
# ==========================================

best_k = max(
    scores,
    key=scores.get
)

best_score = scores[best_k]

print("\n========== BEST CLUSTER COUNT ==========")

print("Best K:", best_k)
print(
    "Best Silhouette Score:",
    f"{best_score:.4f}"
)


# ==========================================
# 5. FINAL K-MEANS MODEL
# ==========================================

kmeans = KMeans(
    n_clusters=best_k,
    random_state=42,
    n_init=20
)

df["cluster"] = kmeans.fit_predict(
    tfidf_matrix
)


# ==========================================
# 6. DISPLAY CLUSTER RESULTS
# ==========================================

print("\n========== CLUSTER RESULTS ==========")

display_columns = [
    "bug_id",
    "title",
    "component",
    "cluster"
]

print(
    df[display_columns]
    .sort_values("cluster")
    .to_string(index=False)
)


# ==========================================
# 7. CLUSTER COUNTS
# ==========================================

print("\n========== CLUSTER COUNTS ==========")

print(
    df["cluster"]
    .value_counts()
    .sort_index()
)


# ==========================================
# 8. EXTRACT CLUSTER KEYWORDS
# ==========================================

print("\n========== CLUSTER KEYWORDS ==========")

terms = vectorizer.get_feature_names_out()

for cluster_number in range(best_k):

    center = kmeans.cluster_centers_[
        cluster_number
    ]

    top_indices = center.argsort()[-10:][::-1]

    keywords = [
        terms[index]
        for index in top_indices
    ]

    print(
        f"\nCluster {cluster_number}:"
    )

    print(
        ", ".join(keywords)
    )


# ==========================================
# 9. SAVE CLUSTERED DATA
# ==========================================

df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\n===================================")
print("Clustered dataset saved successfully!")
print("File:", OUTPUT_PATH)
print("===================================")
