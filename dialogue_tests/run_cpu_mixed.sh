#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
runtime="$project_root/.venv/bin/ltt"

if [[ ! -x "$runtime" ]]; then
  printf 'Brak %s. Utwórz środowisko: python -m venv .venv && .venv/bin/pip install -e .\n' "$runtime" >&2
  exit 1
fi

cd "$project_root"
exec "$runtime" run --experiment dialogue_semantic_baseline
