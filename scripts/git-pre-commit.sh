#!/bin/bash
# Pre-commit: optional venv check + consistency kit.
# Mirrors .github/workflows/ci.yml.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "Checking python dependencies compatibility..."
if [ -x "$ROOT/.venv/bin/pip" ]; then
    if ! "$ROOT/.venv/bin/pip" check; then
        echo "ERROR: Broken requirements found in virtual environment. Commit aborted."
        exit 1
    fi
else
    echo "No .venv/bin/pip — skipping pip check."
fi

# The kit owns version / byte budget / routing surface / count claims /
# reference reachability / declared imports / compilation / CJK encoding.
# Do not write the count here — run `python3 scripts/check_archviz.py --list`.
# This comment has drifted twice already. Config lives in archviz-checks.json.
echo "Checking consistency kit..."
python3 "$ROOT/scripts/check_archviz.py"

echo "Checking consistency kit's own checker..."
python3 "$ROOT/scripts/check_archviz.py" --self-test >/dev/null

# Byte-compilation used to be its own `compileall -q "$ROOT/scripts"
# "$ROOT/archviz_sketch"` step here. It is now the kit's `pycompile` check,
# which walks the whole repo instead of two directories and uses the builtin
# `compile()`, so it leaves no `__pycache__` in the tree it inspects.
