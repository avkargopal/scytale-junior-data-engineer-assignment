# Scytale Junior Data Engineer Assignment

## Overview
This project extracts and analyses GitHub pull requests for the **Scytale-exercise** organisation.
It verifies, for each merged pull request:
- Was it approved by at least one reviewer?
- Did all required status checks pass?

The project follows a simple **ETL pipeline**:
1. **extract.py** – Extracts merged PRs from GitHub and saves raw JSON data.
2. **transform.py** – Transforms the JSON into a CSV report with analysis.

---

## ⚙️ Tech Stack
- Python 3.10+
- requests (for GitHub API calls)
- pandas (for data manipulation and CSV export)
- logging (for visibility)
- dotenv (optional for local environment variables)

---

## 📁 Folder Structure
```
scytale-data-exercise/
├── extract.py
├── transform.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   ├── raw/
│   │   └── prs_raw.json
│   └── output/
│       └── report.csv
```

---

## 🚀 Setup Instructions

### 1️⃣ Clone or open this folder in VS Code
```
git clone https://github.com/<avkargopal>/scytale-junior-data-engineer-assignment.git
cd scytale-junior-data-engineer-assignment
```

### 2️⃣ Create a virtual environment
```
python -m venv .venv
.venv\Scripts\activate
```

### 3️⃣ Install dependencies
```
pip install -r requirements.txt
```
Then set it (PowerShell command):
```
setx GITHUB_TOKEN "your_token_here"
```

Reopen VS Code after setting it.

---

## 🧩 Run the Pipeline

### Step 1: Extract PR Data
```
python extract.py
```
Outputs: `data/raw/prs_raw.json`

### Step 2: Transform & Generate Report
```
python transform.py
```
Outputs: `data/output/report.csv`

---

## 📊 Report Fields
| Column | Description |
|---------|--------------|
| PR_Number | Pull Request number |
| Title | Title of the PR |
| Author | GitHub username of author |
| Merged_At | Merge timestamp |
| CR_Passed | Whether PR was approved by a reviewer |
| Checks_Passed | Whether all status checks succeeded |

---

## 🧠 Notes
- Secrets are never hardcoded; `GITHUB_TOKEN` is read from an environment variable.
- Only `requests` and `pandas` are required.
- Logging is included for debugging and progress tracking.

---

## ✅ Example Output
| PR_Number | Title | Author | Merged_At | CR_Passed | Checks_Passed |
|------------|--------|---------|------------|------------|----------------|
| 14 | Fix API bug | johndoe | 2025-03-21T11:33:00Z | True | True |
| 15 | Add validation | avkar | 2025-03-22T07:10:00Z | True | False |

---

## 👨‍💻 Author
Built by Avkar Gopal for Scytale’s Junior Data Engineer assignment.
