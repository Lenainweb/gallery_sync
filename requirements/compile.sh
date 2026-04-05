#!/bin/bash
set -e
cd "$(dirname $0)"

pip-compile -q --no-emit-index-url --output-file requirements.txt requirements.in