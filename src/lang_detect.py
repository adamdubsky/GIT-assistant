# src/lang_detect.py

from pathlib import PurePath

# Map file extensions → language keys that linter.py understands
EXTENSION_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".go": "go",
    # add more 
}

def extension_to_language(ext: str) -> str:
    """
    Given a file extension (including the leading dot), return the
    normalized language name. Falls back to 'unknown'.
    """
    return EXTENSION_MAP.get(ext, "unknown")
