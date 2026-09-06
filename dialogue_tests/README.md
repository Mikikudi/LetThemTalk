# Testy rozmów LTT

Ten katalog zawiera komplet plików potrzebnych do powtarzalnego testu rozmowy
Bielik–Gemma oraz do ręcznej analizy kierunku znaczenia odpowiedzi.

## Uruchomienie

Z korzenia repozytorium:

```bash
./dialogue_tests/run_cpu_mixed.sh
```

Skrypt wymaga lokalnych modeli GGUF wskazanych w `config/models.yaml` i
środowiska `.venv` utworzonego przez `pip install -e .`. Wynik trafia do
`data/logs/` i `data/sqlite/`; dane te są celowo ignorowane przez Git.

## Co jest mierzone

Test najpierw tylko rejestruje rozmowę. Po jego zakończeniu uruchom:

```bash
./dialogue_tests/inspect_log.py data/logs/<plik>.json
```

Skrypt wyświetla tury oraz szablon adnotacji. Ręcznie przypisz metryki opisane
w `metrics_schema.json`. Nie interpretuj ich jako diagnozy osoby ani modelu.

## Kolejność rozwoju

1. Zbierz kilka powtarzalnych logów i sprawdź zgodność ręcznych adnotacji.
2. Zdefiniuj baseline oraz progi kwantyzacji.
3. Wyliczaj trygram i heksagram wyłącznie jako metadane w logu.
4. Dopiero wtedy testuj wpływ heksagramu na instrukcję dla modelu.

`output/` jest miejscem na lokalne, pochodne raporty i nie trafia do Git.
