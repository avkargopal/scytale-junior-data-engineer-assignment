"""
transform.py
-------------
Reads the raw pull request data from extract.py, then:
    - Checks if each PR was approved by at least one reviewer.
    - Checks if all required status checks passed.
Outputs a CSV summary report.

Inputs:
    data/raw/prs_raw.json
Outputs:
    data/output/report.csv
"""

import os
import json
import requests
import pandas as pd
import logging

# ---------------- CONFIG ---------------- #
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OWNER = "Scytale-exercise"
REPO = "scytale-repo3" 
RAW_FILE = "data/raw/prs_raw.json"
OUTPUT_FILE = "data/output/report.csv"
# ---------------------------------------- #

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

if not GITHUB_TOKEN:
    logging.error("Missing GITHUB_TOKEN environment variable.")
    exit(1)

headers = {"Authorization": f"token {GITHUB_TOKEN}"}
os.makedirs("data/output", exist_ok=True)

def check_reviews(pr_number):
    """Return True if at least one APPROVED review exists."""
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls/{pr_number}/reviews"
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        logging.warning(f"Reviews fetch failed for PR #{pr_number}")
        return False
    reviews = res.json()
    return any(r.get("state") == "APPROVED" for r in reviews)

def check_statuses(statuses_url):
    """Return True if all statuses are 'success'."""
    res = requests.get(statuses_url, headers=headers)
    if res.status_code != 200:
        logging.warning(f"Status check failed: {statuses_url}")
        return False
    statuses = res.json()
    return all(s.get("state") == "success" for s in statuses) if statuses else False

def main():
    with open(RAW_FILE, "r", encoding="utf-8") as f:
        prs = json.load(f)

    results = []
    for pr in prs:
        pr_number = pr["number"]
        title = pr["title"]
        author = pr["user"]["login"]
        merged_at = pr["merged_at"]

        logging.info(f"Processing PR #{pr_number} - {title}")

        cr_passed = check_reviews(pr_number)
        checks_passed = check_statuses(pr["statuses_url"])

        results.append({
            "PR_Number": pr_number,
            "Title": title,
            "Author": author,
            "Merged_At": merged_at,
            "CR_Passed": cr_passed,
            "Checks_Passed": checks_passed
        })

    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_FILE, index=False)
    logging.info(f"✅ Report generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()