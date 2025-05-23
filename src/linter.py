# src/linter.py

import subprocess
from pathlib import Path
from typing import List, Dict

from .lang_detect import extension_to_language

# Map detected language → the linter command (as a list of args)
# Add more, C, C++, C#
LINTER_COMMANDS: Dict[str, List[str]] = {
    "python": ["flake8"],
    "javascript": ["eslint", "--format", "compact"],
    "typescript": ["eslint", "--format", "compact"],
    "go": ["golint"],
}

def lint_files(repo_path: str, files: List[str]) -> Dict[str, str]:
    """
    Run configured linters on the given list of files.

    :param repo_path: Path to the repository root
    :param files: List of file paths (relative to repo_path) to lint
    :return: Mapping from file path → linter output (empty if no issues)
    """
    results: Dict[str, str] = {}
    repo_root = Path(repo_path).resolve()

    for rel_path in files:
        file_path = (repo_root / rel_path).resolve()
        if not file_path.exists():
            results[rel_path] = "⚠ file not found"
            continue

        # detect language by extension
        language = extension_to_language(file_path.suffix.lower())
        cmd = LINTER_COMMANDS.get(language)
        if not cmd:
            results[rel_path] = f"No linter configured for language “{language}”"
            continue

        # run linter
        try:
            completed = subprocess.run(
                cmd + [str(file_path)],
                capture_output=True,
                text=True,
                check=False
            )
            output = (completed.stdout or "") + (completed.stderr or "")
        except Exception as e:
            output = f"Error running linter: {e}"

        results[rel_path] = output.strip()

    return results
