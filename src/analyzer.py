import os
from typing import Dict, Optional
import openai

# Initialize OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Default model and tokens
DEFAULT_MODEL = "gpt-4"
DEFAULT_MAX_TOKENS = 1024


def analyze_diff(
    diff_text: str,
    linter_results: Optional[Dict[str, str]] = None,
    model: str = DEFAULT_MODEL,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> str:
    """
    Send the unified diff (and optional linter output) to OpenAI, returning an analysis string.

    :param diff_text: Unified diff string between two commits
    :param linter_results: Mapping of file path -> linter output
    :param model: OpenAI model to use
    :param max_tokens: Maximum tokens for completion
    :return: The assistant's analysis
    """
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY must be set in environment.")

    # Build the system prompt
    system_message = (
        "You are a senior software engineer assistant. "
        "Given a git diff and optional linter outputs, provide:\n"
        "1. A concise summary of the changes.\n"
        "2. Code quality feedback.\n"
        "3. Potential bugs or edge cases.\n"
        "4. Improvement recommendations."
    )

    # Build the user content
    user_content = f"Here is the diff:\n```diff\n{diff_text}\n```\n"
    if linter_results:
        user_content += "\nLinter results:\n"
        for path, output in linter_results.items():
            snippet = output or "<no issues>"
            user_content += f"- {path}: ```\n{snippet}\n```\n"

    user_message = {
        "role": "user",
        "content": user_content
    }

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            user_message,
        ],
        temperature=0.2,
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content.strip()


def analyze_pr(
    pr_diff: str,
    linter_results: Optional[Dict[str, str]] = None,
    **kwargs
) -> str:
    """
    Alias for analyzing pull request diffs; reuses analyze_diff under the hood.
    """
    return analyze_diff(pr_diff, linter_results, **kwargs)
