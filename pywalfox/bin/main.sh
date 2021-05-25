#!/usr/bin/env bash

# Checks OS Version Number
macOS=$(sw_vers -productVersion)
if [[ ${#macOS} > 0  ]]; then
    PATH="$PATH:/usr/local/bin"
    pywalfox start
fi

python -m pywalfox start || python3 -m pywalfox start || python2.7 -m pywalfox start || python3.9 -m pywalfox start
