# tools/

## `strip_widgets.py` — keep notebooks GitHub-renderable

Colab saves a malformed `metadata.widgets` blob (from progress bars) that makes
GitHub refuse to render the notebook with:

> Invalid Notebook: the 'state' key is missing from 'metadata.widgets'.

This script removes that blob. Code, outputs, and cells are untouched.

```bash
python3 tools/strip_widgets.py            # clean every *.ipynb in the repo
python3 tools/strip_widgets.py a.ipynb    # clean specific files
python3 tools/strip_widgets.py --staged   # clean only git-staged notebooks
```

## Automatic cleaning (pre-commit hook)

`git-hooks/pre-commit` runs the cleaner on staged notebooks before every commit.
It's version-controlled, so activate it once per clone with:

```bash
git config core.hooksPath tools/git-hooks
```

After that, just commit as usual — any notebook you push will render on GitHub.
