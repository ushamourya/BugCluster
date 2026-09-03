# BugCluster
### ML-Based Bug Clustering & Developer Recommendation

### BugCluster is a machine learning project that analyzes software bug reports, groups similar bugs, and recommends a suitable developer for a new bug based on historical bug data.

## 🛠️ Tech Stack

### Programming Language
- Python

### Libraries
- Pandas
- NumPy
- Scikit-learn
- Matplotlib

### Machine Learning Techniques & Metrics
- TF-IDF
- K-Means Clustering
- Silhouette Score
- PCA
- Cosine Similarity

##  Project Structure
```text
BUGCLUSTER/
│
├── data/
│   ├── processed/
│   │   ├── clean_bugs.csv
│   │   ├── clustered_bugs.csv
│   │   ├── bugs_with_developers.csv
│   │   ├── cluster_visualization.png
│   │   └── bug_cluster.png
│   │
│   └── raw/
│       ├── generate_dataset.py
│       └── bugs_large.csv
│
├── ml/
│   ├── preprocessing.py
│   ├── bug_clustering.py
│   ├── cluster_visualization.py
│   ├── developer_assignment.py
│   └── developer_engine.py
│
├── requirements.txt


```
##  Main Files

| File | Purpose |
|---|---|
| `generate_dataset.py` | Generates a synthetic bug dataset and saves it as a CSV file. |
| `preprocessing.py` | Cleans the bug data, handles missing values and duplicates, creates combined bug text, and saves the cleaned dataset. |
| `bug_clustering.py` | Converts bug text into TF-IDF features, selects the best cluster count using Silhouette Score, and groups bugs using K-Means. |
| `cluster_visualization.py` | Uses PCA to reduce TF-IDF features to two dimensions and generates a cluster visualization. |
| `developer_assignment.py` | Assigns developers to historical bugs based on their component and saves the assigned data. |
| `developer_engine.py` | Finds similar historical bugs for a new bug and recommends a developer using component filtering and Cosine Similarity. |

##  Workflow

```text
Generate Synthetic Dataset
          ↓
    Data Preprocessing
          ↓
      TF-IDF Features
          ↓
   K-Means Clustering
          ↓
 Select Best K using
   Silhouette Score
          ↓
   PCA Visualization
          ↓
 Developer Assignment
          ↓
     New Bug Input
          ↓
 Component Selection
          ↓
   TF-IDF + Cosine
      Similarity
          ↓
Find Similar Historical Bugs
          ↓
 Similarity Threshold Check
          ↓
 Developer Recommendation

```
##  Installation
1. Clone the Repository
```
git clone <your-github-repository-url>
cd BUGCLUSTER
```
2. Install Dependencies
```
pip install -r requirements.txt
```
##  Requirements

The project requires:

- pandas
- numpy
- scikit-learn
- matplotlib

##  Running the Project

Run the files in the following order:
```
1. Generate Dataset
python generate_dataset.py
```
```
2. Preprocess Data
python preprocessing.py
```
```
3. Perform Bug Clustering
python bug_clustering.py
```
```
4. Generate Cluster Visualization
python cluster_visualization.py
```
```
5. Assign Developers
python developer_assignment.py
```
```
6. Run Developer Recommendation
python developer_engine.py
```



