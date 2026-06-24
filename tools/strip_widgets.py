#!/usr/bin/env python3
"""Strip Colab's malformed `metadata.widgets` blob from Jupyter notebooks.

Colab records an ipywidgets state object (from tqdm / model-download progress
bars) that is frequently missing its required 'state' key. GitHub's renderer
then refuses to display the notebook ("the 'state' key is missing from
'metadata.widgets'"). This removes the `widgets` metadata at both the notebook
and cell level. Code, outputs, and cell structure are left untouched.

Usage:
    python3 tools/strip_widgets.py                 # every *.ipynb in the repo
    python3 tools/strip_widgets.py a.ipynb b.ipynb # specific files
    python3 tools/strip_widgets.py --staged        # only git-staged *.ipynb
"""
import json
import os
import subprocess
import sys
from glob import glob


def staged_notebooks():
    out = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True, text=True,
    ).stdout
    return [f for f in out.splitlines() if f.endswith(".ipynb") and os.path.exists(f)]


def strip(path):
    """Remove widgets metadata from one notebook. Returns True if it changed."""
    with open(path, encoding="utf-8") as f:
        nb = json.load(f)

    changed = False
    if "widgets" in nb.get("metadata", {}):
        del nb["metadata"]["widgets"]
        changed = True
    for cell in nb.get("cells", []):
        if "widgets" in cell.get("metadata", {}):
            del cell["metadata"]["widgets"]
            changed = True

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
            f.write("\n")
    return changed


def main(argv):
    if "--staged" in argv:
        files = staged_notebooks()
    else:
        explicit = [a for a in argv if a.endswith(".ipynb")]
        files = explicit or sorted(glob("**/*.ipynb", recursive=True))

    cleaned = [f for f in files if strip(f)]
    for f in cleaned:
        print(f"stripped widgets: {f}")
    return cleaned


if __name__ == "__main__":
    main(sys.argv[1:])
