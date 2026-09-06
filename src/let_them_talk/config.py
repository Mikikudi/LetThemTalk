from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class ConfigurationError(ValueError):
    """Konfiguracja eksperymentu jest niekompletna lub niepoprawna."""


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ConfigurationError(f"Brakuje pliku konfiguracji: {path}")
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ConfigurationError(f"Plik musi zawierać mapę YAML: {path}")
    return data


def load_text(project_root: Path, relative_path: str) -> str:
    path = project_root / relative_path
    if not path.is_file():
        raise ConfigurationError(f"Brakuje pliku promptu: {path}")
    return path.read_text(encoding="utf-8").strip()


def load_experiment(project_root: Path, name: str) -> dict[str, Any]:
    models = load_yaml(project_root / "config/models.yaml").get("models", {})
    agents = load_yaml(project_root / "config/agents.yaml").get("agents", {})
    experiments = load_yaml(project_root / "config/experiments.yaml").get("experiments", {})
    experiment = experiments.get(name)
    if not experiment:
        raise ConfigurationError(f"Nie ma eksperymentu: {name}")

    resolved_agents: dict[str, dict[str, Any]] = {}
    for agent_name in ("model_a", "model_b"):
        agent = agents.get(agent_name)
        if not agent:
            raise ConfigurationError(f"Brakuje konfiguracji agenta: {agent_name}")
        overrides = experiment.get("agent_overrides", {}).get(agent_name, {})
        resolved_agent = {**agent, **overrides}
        model_name = resolved_agent.get("model")
        model = models.get(model_name)
        if not model:
            raise ConfigurationError(f"Agent {agent_name} wskazuje nieznany model: {model_name}")
        resolved_agents[agent_name] = {
            **resolved_agent,
            "system_prompt": load_text(project_root, resolved_agent["prompt_file"]),
            "model_config": model,
        }

    return {
        "name": name,
        "task": load_text(project_root, experiment["task_file"]),
        "max_turns": int(experiment.get("max_turns", 12)),
        "consensus_marker": str(experiment.get("consensus_marker", "[KONIEC_DYSKUSJI]")),
        "agents": resolved_agents,
    }
