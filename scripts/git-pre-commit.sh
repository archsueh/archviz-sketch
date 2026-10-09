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

# One kit, seven checks: version / byte budget / routing surface / count claims
# / reference reachability / undeclared imports / CJK encoding. Config lives in
# archviz-checks.json.
echo "Checking consistency kit..."
python3 "$ROOT/scripts/check_archviz.py"

echo "Checking consistency kit's own checker..."
python3 "$ROOT/scripts/check_archviz.py" --self-test >/dev/null

# Note the limit: byte-compilation never *imports*, so it cannot see a missing
# dependency — that is the kit's `deps` check's job, not this one's.
echo "Byte-compiling..."
python3 -m compileall -q "$ROOT/scripts" "$ROOT/archviz_sketch"
