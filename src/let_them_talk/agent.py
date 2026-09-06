from __future__ import annotations

from typing import Protocol


class Runtime(Protocol):
    def complete(self, messages: list[dict[str, str]], *, temperature: float, max_tokens: int) -> str: ...


class Agent:
    def __init__(self, name: str, runtime: Runtime, system_prompt: str, temperature: float, max_tokens: int) -> None:
        self.name = name
        self.runtime = runtime
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.max_tokens = max_tokens

    def respond(self, task: str, transcript: list[dict[str, str]]) -> str:
        lines = [f"Zadanie eksperymentu:\n{task}", "\nDotychczasowa dyskusja:"]
        lines.extend(f"[{turn['speaker']}]: {turn['content']}" for turn in transcript)
        lines.append(f"\nTeraz odpowiadasz jako {self.name}. Nie przypisuj sobie cudzych wypowiedzi.")
        return self.runtime.complete(
            [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": "\n".join(lines)},
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
