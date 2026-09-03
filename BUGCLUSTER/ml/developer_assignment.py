import pandas as pd


# ==========================================================
# BugCluster - Developer Assignment
# ==========================================================

INPUT_PATH = "../data/processed/clustered_bugs.csv"
OUTPUT_PATH = "../data/processed/bugs_with_developers.csv"


# ==========================================================
# 1. DEVELOPER MAPPING
# ==========================================================

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


# ==========================================================
# 2. LOAD CLUSTERED BUG DATA
# ==========================================================

print("========================================")
print("Loading clustered bug data...")
print("========================================")

try:

    df = pd.read_csv(INPUT_PATH)

except FileNotFoundError:

    print("\nERROR:")
    print("File not found:")
    print(INPUT_PATH)

    print("\nPlease run these files first:")
    print("1. generate_dataset.py")
    print("2. preprocessing.py")
    print("3. bug_clustering.py")

    exit()


print("\nClustered dataset loaded successfully!")

print(
    "Number of bugs:",
    len(df)
)


# ==========================================================
# 3. CHECK COMPONENT COLUMN
# ==========================================================

if "component" not in df.columns:

    print("\nERROR:")
    print("'component' column is missing.")

    exit()


# ==========================================================
# 4. ASSIGN DEVELOPERS
# ==========================================================

df["developer"] = (
    df["component"]
    .map(COMPONENT_DEVELOPERS)
)


# ==========================================================
# 5. CHECK UNKNOWN COMPONENTS
# ==========================================================

unknown_components = df[
    df["developer"].isna()
]


if len(unknown_components) > 0:

    print("\n========================================")
    print("WARNING")
    print("========================================")

    print(
        "Some bugs do not have a developer assignment."
    )

    print(
        unknown_components[
            [
                "bug_id",
                "title",
                "component"
            ]
        ].to_string(index=False)
    )

else:

    print(
        "\nAll bugs have developer assignments."
    )


# ==========================================================
# 6. DISPLAY ASSIGNMENTS
# ==========================================================

print("\n========================================")
print("BUG DEVELOPER ASSIGNMENTS")
print("========================================")

display_columns = [
    "bug_id",
    "title",
    "component",
    "cluster",
    "developer"
]


print(
    df[
        display_columns
    ]
    .to_string(index=False)
)


# ==========================================================
# 7. DEVELOPER WORKLOAD
# ==========================================================

print("\n========================================")
print("DEVELOPER WORKLOAD")
print("========================================")

workload = (
    df["developer"]
    .value_counts()
    .sort_index()
)


print(workload)


# ==========================================================
# 8. COMPONENT SUMMARY
# ==========================================================

print("\n========================================")
print("COMPONENT - DEVELOPER SUMMARY")
print("========================================")

for component, developer in COMPONENT_DEVELOPERS.items():

    bug_count = len(
        df[
            df["component"] == component
        ]
    )

    print(
        f"{component:<20} → "
        f"{developer:<10} "
        f"({bug_count} bugs)"
    )


# ==========================================================
# 9. SAVE DATA
# ==========================================================

df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ==========================================================
# 10. COMPLETION MESSAGE
# ==========================================================

print("\n========================================")
print("Developer assignment completed!")
print("========================================")

print(
    "Output file:",
    OUTPUT_PATH
)

print(
    "Total bugs:",
    len(df)
)

print("========================================")
