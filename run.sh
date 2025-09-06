#!/bin/bash

cd SimpleSites

if [[ "$(uname)" == "Darwin" ]]; then
    python3 ./watch.py
else
    python3 ./watch.py
fi
 