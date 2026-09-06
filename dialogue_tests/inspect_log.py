#!/usr/bin/env python3
"""Wyświetla transcript LTT i szablon ręcznej adnotacji dla każdej tury."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Użycie: ./dialogue_tests/inspect_log.py data/logs/<eksperyment>.json")
    path = Path(sys.argv[1])
    payload = json.loads(path.read_text(encoding="utf-8"))
    print(f"Eksperyment: {payload['experiment_id']}")
    for index, turn in enumerate(payload["turns"], start=1):
        print(f"\n[{index}] {turn['speaker']} | runda {turn['round']} | {turn['elapsed_ms']} ms")
        print(turn["content"])
        print("Adnotacja: etymologia_bit=? d_czas=? d_znaczenie=? d_geografia=? rytm=?")


if __name__ == "__main__":
    main()
