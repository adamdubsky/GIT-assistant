# src/watcher.py
#git commit --allow-empty -m "Test local"
import time
import logging
from pathlib import Path
from git import Repo, GitCommandError

# How often to check for new commits (in secs)
POLL_INTERVAL = 3 #Often for testing, but should be longer in production

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

def monitor_repo(path: str):
    """
    Watch a Git repo for new local or remote commits and include their hashes.

    :param path: Filesystem path to a Git repository
    """
    repo_path = Path(path).expanduser().resolve()
    repo = Repo(repo_path)
    branch_name = repo.active_branch.name

    last_local_sha = repo.head.commit.hexsha
    # initialize last_remote to current remote tip
    try:
        repo.remotes.origin.fetch()
        last_remote_sha = repo.remotes.origin.refs[branch_name].commit.hexsha
    except GitCommandError as e:
        logger.warning("Initial remote fetch failed: %s", e)
        last_remote_sha = None

    logger.info(f"Watching {repo_path} on branch '{branch_name}'")
    while True:
        try:
            # fetch updates from origin
            repo.remotes.origin.fetch()
            remote_head = repo.remotes.origin.refs[branch_name].commit.hexsha
        except GitCommandError as e:
            logger.error("Remote fetch error: %s", e)
            remote_head = None

        # check for incoming commits
        if remote_head and remote_head != last_remote_sha:
            logger.info(f"🔽 Detected new remote commit: {remote_head}")
            # TODO: hand off to diff_parser & analyzer
            last_remote_sha = remote_head

        # check for new local commits
        local_head = repo.head.commit.hexsha
        if local_head != last_local_sha:
            logger.info(f"🔼 Detected new local commit: {local_head}")
            # TODO: hand off to diff_parser & analyzer
            last_local_sha = local_head

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description="Watch a Git repo for new commits and log their hashes")
    p.add_argument("path", nargs="?", default=".", help="Path to the Git repository")
    args = p.parse_args()

    monitor_repo(args.path)
