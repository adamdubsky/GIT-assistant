# src/pr_fetcher.py

import os
import requests
from typing import List, Dict, Optional

# Configuration via environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")           # Your GitHub personal access token
GITHUB_OWNER = os.getenv("GITHUB_OWNER")           # e.g. "your-username" or org name
GITHUB_REPO  = os.getenv("GITHUB_REPO")            # e.g. "git-watcher"
API_BASE     = "https://api.github.com"

# Common headers for authenticated requests
HEADERS = {
    **({"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}),
    "Accept": "application/vnd.github.v3+json"
}


def fetch_open_prs(
    owner: Optional[str] = None,
    repo:  Optional[str] = None
) -> List[Dict]:
    """
    Return a list of open pull requests for the given repo.
    Each PR dict includes fields like "number", "title", etc.
    """
    owner = owner or GITHUB_OWNER
    repo  = repo  or GITHUB_REPO
    if not owner or not repo:
        raise ValueError("GITHUB_OWNER and GITHUB_REPO must be set (or passed as args)")
    url = f"{API_BASE}/repos/{owner}/{repo}/pulls?state=open"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


def fetch_pr_diff(
    pr_number: int,
    owner:      Optional[str] = None,
    repo:       Optional[str] = None
) -> str:
    """
    Fetch the unified diff for a specific pull request.
    """
    owner = owner or GITHUB_OWNER
    repo  = repo  or GITHUB_REPO
    url = f"{API_BASE}/repos/{owner}/{repo}/pulls/{pr_number}"
    headers = {**HEADERS, "Accept": "application/vnd.github.v3.diff"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.text


def get_open_pr_diffs(
    owner: Optional[str] = None,
    repo:  Optional[str] = None
) -> List[Dict[str, str]]:
    """
    Returns a list of dicts, each containing:
      - number: PR number
      - title:  PR title
      - diff:   unified diff as a string
    """
    prs = fetch_open_prs(owner, repo)
    results: List[Dict[str, str]] = []
    for pr in prs:
        num   = pr["number"]
        title = pr.get("title", "")
        diff  = fetch_pr_diff(num, owner, repo)
        results.append({"number": num, "title": title, "diff": diff})
    return results
