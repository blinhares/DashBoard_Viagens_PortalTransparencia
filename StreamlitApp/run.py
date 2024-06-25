# we need to import the main.py file to
# ensure that PyInstaller includes it in the build
import main # type: ignore

import streamlit.web.cli as stcli
import os
import sys


def resolve_path(path: str) -> str:
    """Resolve a path relative to this file's location."""
    resolved_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), path))
    return resolved_path


if __name__ == "__main__":
    sys.argv = [
        "streamlit",
        "run",
        resolve_path("main.py"),
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main())
