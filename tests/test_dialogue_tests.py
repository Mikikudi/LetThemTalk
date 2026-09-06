from pathlib import Path
import unittest

from let_them_talk.config import load_experiment


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class DialogueTestsConfigurationTests(unittest.TestCase):
    def test_dialogue_baseline_profile_resolves(self) -> None:
        config = load_experiment(PROJECT_ROOT, "dialogue_semantic_baseline")

        self.assertEqual(config["max_turns"], 3)
        self.assertEqual(config["agents"]["model_a"]["temperature"], 0.2)
        self.assertEqual(config["agents"]["model_b"]["max_tokens"], 180)
