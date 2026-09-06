from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def save_experiment(project_root: Path, config: dict[str, Any], turns: list[dict[str, object]], ended_by_consensus: bool) -> tuple[Path, str]:
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    experiment_id = f"{config['name']}-{timestamp}"
    payload = {
        "experiment_id": experiment_id,
        "created_at": timestamp,
        "config": config,
        "ended_by_consensus": ended_by_consensus,
        "turns": turns,
    }
    logs_dir = project_root / "data/logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    json_path = logs_dir / f"{experiment_id}.json"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    database_path = project_root / "data/sqlite/let_them_talk.db"
    database_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database_path) as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS experiments (
                id TEXT PRIMARY KEY, created_at TEXT NOT NULL, config_json TEXT NOT NULL,
                ended_by_consensus INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS turns (
                experiment_id TEXT NOT NULL, turn_index INTEGER NOT NULL, round_number INTEGER NOT NULL,
                speaker TEXT NOT NULL, content TEXT NOT NULL, elapsed_ms REAL NOT NULL,
                PRIMARY KEY (experiment_id, turn_index)
            );
            """
        )
        connection.execute(
            "INSERT INTO experiments VALUES (?, ?, ?, ?)",
            (experiment_id, timestamp, json.dumps(config, ensure_ascii=False), int(ended_by_consensus)),
        )
        connection.executemany(
            "INSERT INTO turns VALUES (?, ?, ?, ?, ?, ?)",
            [
                (experiment_id, index, turn["round"], turn["speaker"], turn["content"], turn["elapsed_ms"])
                for index, turn in enumerate(turns, start=1)
            ],
        )
    return json_path, experiment_id
