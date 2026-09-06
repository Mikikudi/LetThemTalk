import unittest
from pathlib import Path

from let_them_talk.config import load_experiment


class ConfigTests(unittest.TestCase):
    def test_smoke_profile_limits_tokens(self):
        root = Path(__file__).resolve().parents[1]
        config = load_experiment(root, "bielik_smoke")
        self.assertEqual(1, config["max_turns"])
        self.assertEqual(160, config["agents"]["model_a"]["max_tokens"])
        self.assertEqual(160, config["agents"]["model_b"]["max_tokens"])

    def test_gemma_profile_uses_gemma_model(self):
        root = Path(__file__).resolve().parents[1]
        config = load_experiment(root, "gemma_smoke")
        self.assertEqual("gemma_gguf", config["agents"]["model_a"]["model"])
        self.assertEqual("gemma_gguf", config["agents"]["model_b"]["model"])
        self.assertIn("gemma-4-e4b-it", config["agents"]["model_a"]["model_config"]["path"])

    def test_mixed_profile_has_distinct_models_and_personas(self):
        root = Path(__file__).resolve().parents[1]
        config = load_experiment(root, "history_architecture_mixed_smoke")
        self.assertNotEqual(config["agents"]["model_a"]["model"], config["agents"]["model_b"]["model"])
        self.assertIn("polonistą", config["agents"]["model_a"]["system_prompt"])
        self.assertIn("architektem", config["agents"]["model_b"]["system_prompt"])

    def test_long_mixed_profile_has_six_utterances(self):
        root = Path(__file__).resolve().parents[1]
        config = load_experiment(root, "history_architecture_mixed_long")
        self.assertEqual(3, config["max_turns"])
