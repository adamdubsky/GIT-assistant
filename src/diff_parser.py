from git import Repo
from pathlib import Path

def get_diff(repo_path: str, sha_old: str, sha_new: str) -> str:
    """
    Return the unified diff between two commits.

    :param repo_path: path to the git repository
    :param sha_old: base commit SHA
    :param sha_new: head commit SHA
    :return: unified diff as a single string
    """
    repo = Repo(Path(repo_path))
    
    diff_index = repo.git.diff(f"{sha_old}..{sha_new}", unified=3)
    return diff_index
