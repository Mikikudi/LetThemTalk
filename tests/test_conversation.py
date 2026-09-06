import unittest

from let_them_talk.conversation import run_conversation


class FakeAgent:
    def __init__(self, name, answers):
        self.name = name
        self.answers = iter(answers)

    def respond(self, task, transcript):
        return next(self.answers)


class ConversationTests(unittest.TestCase):
    def test_only_model_b_can_end_by_consensus(self):
        a = FakeAgent("model_a", ["[KONIEC_DYSKUSJI]", "kolejna uwaga"])
        b = FakeAgent("model_b", ["plan [KONIEC_DYSKUSJI]"])
        result = run_conversation(a, b, "zadanie", 3, "[KONIEC_DYSKUSJI]")
        self.assertTrue(result.ended_by_consensus)
        self.assertEqual(2, len(result.turns))

    def test_limit_ends_conversation(self):
        a = FakeAgent("model_a", ["a1", "a2"])
        b = FakeAgent("model_b", ["b1", "b2"])
        result = run_conversation(a, b, "zadanie", 2, "[KONIEC_DYSKUSJI]")
        self.assertFalse(result.ended_by_consensus)
        self.assertEqual(4, len(result.turns))
