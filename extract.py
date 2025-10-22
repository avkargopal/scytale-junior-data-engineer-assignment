"""
extract.py
-----------
Fetch merged pull requests from a GitHub repository under the Scytale-exercise org.
Authenticates using a personal access token (PAT) stored in the GITHUB_TOKEN environment variable.
Saves merged pull requests as JSON for downstream processing.

Outputs:
    data/raw/prs_raw.json
"""

import os
import requests
import json
import logging

# ---------------- CONFIG ---------------- #
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OWNER = "Scytale-exercise"
REPO = "scytale-repo3"  
OUTPUT_FILE = "data/raw/prs_raw.json"
PER_PAGE = 100  # Max allowed per page
# ---------------------------------------- #

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

if not GITHUB_TOKEN:
    logging.error("Missing GITHUB_TOKEN environment variable.")
    exit(1)

os.makedirs("data/raw", exist_ok=True)
headers = {"Authorization": f"token {GITHUB_TOKEN}"}

def fetch_merged_prs():
    """Fetch all merged pull requests, handling pagination."""
    page = 1
    merged_prs = []

    while True:
        url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls?state=closed&per_page={PER_PAGE}&page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            logging.error(f"GitHub API error {response.status_code}: {response.text}")
            break

        prs = response.json()
        if not prs:
            break

        merged = [pr for pr in prs if pr.get("merged_at")]
        merged_prs.extend(merged)
        logging.info(f"Page {page}: found {len(merged)} merged PRs")
        page += 1

    return merged_prs

def main():
    logging.info(f"Fetching merged PRs for {OWNER}/{REPO}...")
    merged_prs = fetch_merged_prs()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(merged_prs, f, indent=2)

    logging.info(f"✅ Saved {len(merged_prs)} merged PRs to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()