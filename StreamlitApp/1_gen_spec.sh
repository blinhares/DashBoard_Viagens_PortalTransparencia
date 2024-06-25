#!/bin/sh
# Generate spec file, then modify it
pyinstaller --onefile --additional-hooks-dir=./hooks main.py --clean
