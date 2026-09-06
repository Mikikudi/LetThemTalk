import sqlite3
import tempfile
import unittest
from pathlib import Path

from let_them_talk.storage import save_experiment


class StorageTests(unittest.TestCase):
    def test_saves_json_and_sqlite(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            log_path, experiment_id = save_experiment(
                root, {"name": "test"}, [{"round": 1, "speaker": "a", "content": "tekst", "elapsed_ms": 1.0}], True
            )
            self.assertTrue(log_path.is_file())
            with sqlite3.connect(root / "data/sqlite/let_them_talk.db") as connection:
                self.assertEqual(experiment_id, connection.execute("SELECT id FROM experiments").fetchone()[0])
