import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# BugCluster - Developer Recommendation Engine
# ============================================================

DATA_PATH = "../data/processed/bugs_with_developers.csv"

# Minimum similarity required for a reliable recommendation
MIN_SIMILARITY = 0.05


# ============================================================
# COMPONENT -> DEVELOPER MAPPING
# ============================================================

COMPONENT_DEVELOPERS = {
    "Authentication": "Rahul",
    "Payment": "Arjun",
    "Frontend": "Sneha",
    "Dashboard": "Priya",
    "Search": "Vikram",
    "Notifications": "Priya",
    "API": "Arjun",
    "Database": "Vikram",
    "Performance": "Priya",
    "File Upload": "Sneha"
}


COMPONENTS = list(COMPONENT_DEVELOPERS.keys())


# ============================================================
# 1. LOAD DATA
# ============================================================

try:

    df = pd.read_csv(DATA_PATH)

except FileNotFoundError:

    print("\nERROR:")
    print("Could not find:")
    print(DATA_PATH)

    print("\nPlease run developer_engine.py after:")
    print("1. generate_dataset.py")
    print("2. preprocessing.py")
    print("3. bug_clustering.py")
    print("4. developer_engine.py data preparation")

    exit()


print("========================================")
print("Bug history loaded successfully!")
print("Number of bugs:", len(df))
print("========================================")


# ============================================================
# 2. CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "bug_id",
    "title",
    "component",
    "developer",
    "bug_text"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    print("\nERROR: Missing columns:")

    for column in missing_columns:
        print("-", column)

    exit()


# ============================================================
# 3. CLEAN BUG TEXT
# ============================================================

df["bug_text"] = (
    df["bug_text"]
    .fillna("")
    .astype(str)
)

df["component"] = (
    df["component"]
    .fillna("Unknown")
    .astype(str)
)

df["developer"] = (
    df["developer"]
    .fillna("Unknown")
    .astype(str)
)


# ============================================================
# 4. CREATE TF-IDF FEATURES
# ============================================================

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


# ============================================================
# 5. DISPLAY COMPONENT OPTIONS
# ============================================================

print("\n========================================")
print("SELECT BUG COMPONENT(S)")
print("========================================")

for index, component in enumerate(COMPONENTS, start=1):

    print(
        f"{index}. {component} "
        f"→ {COMPONENT_DEVELOPERS[component]}"
    )


print(f"{len(COMPONENTS) + 1}. Other / Unexpected")


# ============================================================
# 6. GET COMPONENT SELECTION
# ============================================================

while True:

    selection = input(
        "\nEnter component number(s), separated by comma: "
    ).strip()

    if not selection:
        print("Please select at least one component.")
        continue

    try:

        numbers = [
            int(value.strip())
            for value in selection.split(",")
        ]

    except ValueError:

        print(
            "Invalid input. Example: 2 "
            "or 2,3"
        )

        continue


    valid = True

    selected_components = []


    for number in numbers:

        if number < 1 or number > len(COMPONENTS) + 1:

            valid = False
            break


        # Other / Unexpected
        if number == len(COMPONENTS) + 1:

            selected_components.append("Other")

        else:

            component = COMPONENTS[number - 1]

            if component not in selected_components:

                selected_components.append(component)


    if valid:
        break

    print("Invalid component number.")


# ============================================================
# 7. DISPLAY SELECTED COMPONENTS
# ============================================================

print("\n========================================")
print("SELECTED COMPONENT(S)")
print("========================================")

for component in selected_components:

    if component == "Other":

        print(
            "Other / Unexpected"
        )

    else:

        print(
            f"{component} "
            f"→ {COMPONENT_DEVELOPERS[component]}"
        )


# ============================================================
# 8. GET BUG DESCRIPTION
# ============================================================

print("\n========================================")
print("NEW BUG DESCRIPTION")
print("========================================")

while True:

    new_bug = input(
        "\nEnter the bug description:\n"
    ).strip()

    if new_bug:

        break

    print(
        "Bug description cannot be empty."
    )


# ============================================================
# 9. TRANSFORM NEW BUG
# ============================================================

new_bug_vector = vectorizer.transform(
    [new_bug]
)


# ============================================================
# 10. CALCULATE COSINE SIMILARITY
# ============================================================

similarities = cosine_similarity(
    new_bug_vector,
    tfidf_matrix
)[0]

df["similarity"] = similarities


# ============================================================
# 11. FILTER BY SELECTED COMPONENTS
# ============================================================

known_components = [
    component
    for component in selected_components
    if component != "Other"
]


if known_components:

    filtered_df = df[
        df["component"].isin(
            known_components
        )
    ].copy()

else:

    # If only Other was selected,
    # search the complete historical dataset

    filtered_df = df.copy()


# ============================================================
# 12. CHECK IF HISTORICAL BUGS EXIST
# ============================================================

if filtered_df.empty:

    print("\n========================================")
    print("NO HISTORICAL BUGS FOUND")
    print("========================================")

    print(
        "There are no historical bugs for "
        "the selected component(s)."
    )

    print(
        "\nPlease assign the bug manually."
    )

    exit()


# ============================================================
# 13. GET TOP SIMILAR BUGS
# ============================================================

top_bugs = (
    filtered_df
    .sort_values(
        by="similarity",
        ascending=False
    )
    .head(5)
    .copy()
)


# ============================================================
# 14. DISPLAY SIMILAR BUGS
# ============================================================

print("\n========================================")
print("SIMILAR HISTORICAL BUGS")
print("========================================")

display_columns = [
    "bug_id",
    "title",
    "component",
    "developer",
    "similarity"
]

print(
    top_bugs[
        display_columns
    ].to_string(index=False)
)


# ============================================================
# 15. CHECK BEST SIMILARITY
# ============================================================

best_similarity = (
    top_bugs.iloc[0]["similarity"]
)


print("\n========================================")
print("SIMILARITY CHECK")
print("========================================")

print(
    "Best similarity:",
    f"{best_similarity:.4f}"
)

print(
    "Minimum required:",
    f"{MIN_SIMILARITY:.4f}"
)


# ============================================================
# 16. DEVELOPER RECOMMENDATION
# ============================================================

developer_scores = {}


for _, bug in top_bugs.iterrows():

    developer = bug["developer"]

    similarity = bug["similarity"]


    if developer == "Unknown":
        continue


    if developer not in developer_scores:

        developer_scores[developer] = 0.0


    developer_scores[developer] += similarity


# ============================================================
# 17. HANDLE NO RELIABLE MATCH
# ============================================================

if best_similarity < MIN_SIMILARITY:

    print("\n========================================")
    print("NO RELIABLE HISTORICAL MATCH")
    print("========================================")

    print(
        "The new bug does not sufficiently "
        "match the historical bug data."
    )

    print(
        "\nPlease provide more detailed information "
        "or assign the bug manually."
    )

    exit()


# ============================================================
# 18. DISPLAY DEVELOPER SCORES
# ============================================================

print("\n========================================")
print("DEVELOPER SCORES")
print("========================================")

sorted_developers = sorted(
    developer_scores.items(),
    key=lambda x: x[1],
    reverse=True
)


for developer, score in sorted_developers:

    print(
        f"{developer}: {score:.4f}"
    )


# ============================================================
# 19. FINAL RECOMMENDATION
# ============================================================

if not sorted_developers:

    print("\n========================================")
    print("NO DEVELOPER RECOMMENDATION")
    print("========================================")

    print(
        "No developer could be identified."
    )

    exit()


recommended_developer = (
    sorted_developers[0][0]
)


# ============================================================
# 20. DISPLAY FINAL RESULT
# ============================================================

print("\n========================================")
print("DEVELOPER RECOMMENDATION")
print("========================================")


if known_components:

    print(
        "\nSelected Component(s):"
    )

    for component in known_components:

        print(
            f"- {component}"
        )


print(
    "\nRecommended Developer:",
    recommended_developer
)


# ============================================================
# 21. SHOW ADDITIONAL DEVELOPERS
# ============================================================

if len(sorted_developers) > 1:

    print(
        "\nOther possible developers:"
    )

    for developer, score in sorted_developers[1:]:

        print(
            f"- {developer}: "
            f"{score:.4f}"
        )


# ============================================================
# 22. SHOW REASON
# ============================================================

print("\nReason:")

if known_components:

    print(
        "The developer was recommended based on "
        "the selected component(s) and similarity "
        "to historical bugs."
    )

else:

    print(
        "The developer was recommended based on "
        "similarity to historical bugs."
    )


print("\n========================================")
print("Recommendation process completed.")
print("========================================")
