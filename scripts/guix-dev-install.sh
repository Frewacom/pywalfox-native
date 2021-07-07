#!/bin/sh

# Get path of script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Create install dir
mkdir -p ~/.local/lib/python3.8/site-packages

# Build and install executable
python3 $SCRIPT_DIR/../setup.py install --prefix=~/.local
