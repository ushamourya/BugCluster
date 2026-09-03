import pandas as pd
import numpy as np

# ==============================
# BugCluster - Data Preprocessing
# ==============================

DATA_PATH = "../data/raw/bugs_large.csv"
OUTPUT_PATH = "../data/processed/clean_bugs.csv"


# ==================================
# 1. LOAD BUG DATA
# ==================================

df = pd.read_csv(DATA_PATH)

print("========== INITIAL DATA ==========")
print("Dataset shape:", df.shape)

print("\nFirst 5 bugs:")
print(df.head())


# ==================================
# 2. CHECK COLUMNS
# ==================================

print("\nColumns:")
print(df.columns.tolist())


# ==================================
# 3. CHECK MISSING VALUES
# ==================================

print("\nMissing values:")
print(df.isnull().sum())


# ==================================
# 4. CHECK DUPLICATES
# ==================================

print("\nDuplicate rows:", df.duplicated().sum())

print(
    "Duplicate bug IDs:",
    df["bug_id"].duplicated().sum()
)


# ==================================
# 5. HANDLE MISSING TEXT VALUES
# ==================================

df["title"] = df["title"].fillna("")
df["description"] = df["description"].fillna("")


# ==================================
# 6. HANDLE CATEGORICAL VALUES
# ==================================

categorical_columns = [
    "priority",
    "severity",
    "component",
    "status",
    "developer"
]

for column in categorical_columns:

    if column in df.columns:
        df[column] = df[column].fillna("Unknown")


# ==================================
# 7. REMOVE DUPLICATE ROWS
# ==================================

df = df.drop_duplicates()


# ==================================
# 8. REMOVE DUPLICATE BUG IDs
# ==================================

df = df.drop_duplicates(
    subset=["bug_id"],
    keep="first"
)


# ==================================
# 9. CREATE COMBINED BUG TEXT
# ==================================

df["bug_text"] = (
    df["title"] + " " +
    df["description"]
)


# ==================================
# 10. CLEAN BUG TEXT
# ==================================

df["bug_text"] = (
    df["bug_text"]
    .str.lower()
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)


# ==================================
# 11. BASIC DATA ANALYSIS
# ==================================

print("\n========== BUG ANALYSIS ==========")


print("\nBugs by Priority:")
print(
    df["priority"].value_counts()
)


print("\nBugs by Severity:")
print(
    df["severity"].value_counts()
)


print("\nBugs by Component:")
print(
    df["component"].value_counts()
)


print("\nBugs by Status:")
print(
    df["status"].value_counts()
)


if "developer" in df.columns:

    print("\nBugs by Developer:")
    print(
        df["developer"].value_counts()
    )


# ==================================
# 12. FINAL CLEANED DATA
# ==================================

print("\n========== CLEANED DATA ==========")

print("\nCleaned bug text:")
print(
    df[
        ["bug_id", "bug_text"]
    ].head()
)


print("\nFinal dataset shape:")
print(df.shape)


print("\nMissing values after cleaning:")
print(df.isnull().sum())


# ==================================
# 13. SAVE CLEANED DATA
# ==================================

df.to_csv(
    OUTPUT_PATH,
    index=False
)


print("\n===================================")
print("Cleaned dataset saved successfully!")
print("File:", OUTPUT_PATH)
print("===================================")
