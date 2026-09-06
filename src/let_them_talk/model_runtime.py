from __future__ import annotations

from pathlib import Path
from typing import Any


class LlamaCppRuntime:
    """Cienki adapter, aby logika rozmowy nie zależała od llama.cpp."""

    def __init__(self, model_config: dict[str, Any]) -> None:
        path = Path(model_config["path"]).expanduser()
        if not path.is_file():
            raise FileNotFoundError(f"Nie znaleziono modelu GGUF: {path}")
        try:
            from llama_cpp import Llama
        except ImportError as error:
            raise RuntimeError("Zainstaluj zależności: pip install -e .") from error
        self._model = Llama(
            model_path=str(path),
            n_ctx=int(model_config.get("n_ctx", 8192)),
            n_threads=int(model_config.get("n_threads", 8)),
            n_batch=int(model_config.get("n_batch", 512)),
            n_gpu_layers=int(model_config.get("n_gpu_layers", 0)),
            verbose=False,
        )

    def complete(self, messages: list[dict[str, str]], *, temperature: float, max_tokens: int) -> str:
        response = self._model.create_chat_completion(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response["choices"][0]["message"]["content"].strip()
