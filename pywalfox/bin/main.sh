#!/usr/bin/env bash

# Extend PATH for Homebrew (macOS and Linux) and common user locations
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS Homebrew paths
    PATH="$PATH:/usr/local/bin:/opt/homebrew/bin"
else
    # Linux Homebrew path
    PATH="$PATH:/home/linuxbrew/.linuxbrew/bin"
fi
# User pip installs and other common locations
PATH="$PATH:$HOME/.local/bin"

# Try pywalfox directly first (works with pipx and standard pip install)
# Fall back to python module invocation for edge cases
pywalfox start 2>/dev/null || \
    python3 -m pywalfox start 2>/dev/null || \
    python -m pywalfox start 2>/dev/null || \
    echo "Failed to start pywalfox daemon" >&2
