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

# One kit, five checks: version / byte budget / routing surface / count claims
# / CJK encoding. Config lives in archviz-checks.json.
echo "Checking consistency kit..."
python3 "$ROOT/scripts/check_archviz.py"

echo "Checking consistency kit's own checker..."
python3 "$ROOT/scripts/check_archviz.py" --self-test >/dev/null
