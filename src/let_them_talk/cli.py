from __future__ import annotations

import argparse
from pathlib import Path

from .agent import Agent
from .config import ConfigurationError, load_experiment
from .conversation import run_conversation
from .model_runtime import LlamaCppRuntime
from .storage import save_experiment


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    parser = argparse.ArgumentParser(description="Lokalny eksperyment rozmowy modeli GGUF.")
    parser.add_argument("command", choices=["run"])
    parser.add_argument("--experiment", default="secure_local_llm")
    args = parser.parse_args()
    try:
        config = load_experiment(PROJECT_ROOT, args.experiment)
        runtimes: dict[str, LlamaCppRuntime] = {}
        agents: list[Agent] = []
        for name in ("model_a", "model_b"):
            agent_config = config["agents"][name]
            model_name = agent_config["model"]
            runtime = runtimes.get(model_name)
            if runtime is None:
                runtime = LlamaCppRuntime(agent_config["model_config"])
                runtimes[model_name] = runtime
            agents.append(Agent(name, runtime, agent_config["system_prompt"], agent_config["temperature"], agent_config["max_tokens"]))
        result = run_conversation(agents[0], agents[1], config["task"], config["max_turns"], config["consensus_marker"])
        log_path, experiment_id = save_experiment(PROJECT_ROOT, config, result.turns, result.ended_by_consensus)
        print(f"Zapisano eksperyment {experiment_id}: {log_path}")
    except (ConfigurationError, FileNotFoundError, RuntimeError) as error:
        raise SystemExit(f"Błąd: {error}") from error


if __name__ == "__main__":
    main()
