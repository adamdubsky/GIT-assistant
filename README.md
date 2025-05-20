# GIT-assistant

A terminal-based tool that monitors a local Git repository for new local and remote commits, extracts diffs, runs traditional linters, and leverages the OpenAI API to generate actionable, AI-powered insights on code changes and pull requests.

---

## Features

- Real-time commit monitoring: Polls both local and remote branches for new commits.
- Unified diff extraction: Captures the diff between commits for analysis.
- Language detection: Automatically infers programming languages from file extensions.
- Linter integration: Runs linters (e.g., Flake8, ESLint) against changed files and aggregates results.
- AI-driven analysis: Uses OpenAI's GPT model to provide context-aware summaries, code quality feedback, and architectural observations on diffs and PRs.
- PR support: Fetches and analyzes pull requests from GitHub (or GitLab with minimal adjustments).
- Configurable polling interval and command-line options.

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/git-watcher.git
cd git-watcher
