from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Protocol


class ConversationalAgent(Protocol):
    name: str

    def respond(self, task: str, transcript: list[dict[str, str]]) -> str: ...


@dataclass
class ConversationResult:
    turns: list[dict[str, object]]
    ended_by_consensus: bool


def run_conversation(
    agent_a: ConversationalAgent,
    agent_b: ConversationalAgent,
    task: str,
    max_turns: int,
    consensus_marker: str,
) -> ConversationResult:
    transcript: list[dict[str, object]] = []
    for round_number in range(1, max_turns + 1):
        for agent in (agent_a, agent_b):
            started = perf_counter()
            answer = agent.respond(task, transcript)  # type: ignore[arg-type]
            elapsed_ms = round((perf_counter() - started) * 1000, 1)
            if not answer:
                raise RuntimeError(f"{agent.name} zwrócił pustą odpowiedź.")
            turn = {
                "round": round_number,
                "speaker": agent.name,
                "content": answer,
                "elapsed_ms": elapsed_ms,
            }
            transcript.append(turn)
            if agent is agent_b and consensus_marker in answer:
                return ConversationResult(transcript, ended_by_consensus=True)
    return ConversationResult(transcript, ended_by_consensus=False)
