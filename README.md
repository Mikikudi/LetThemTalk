# LetThemTalk

Lokalne laboratorium do powtarzalnych dyskusji między modelami językowymi.

Pierwsza wersja działa wyłącznie przez `llama-cpp-python` i modele GGUF. 
runtime na późniejszy etap.

## Uruchomienie

1. Utwórz środowisko Python i zainstaluj projekt:

   ```bash
   python -m venv .venv
   .venv/bin/pip install -e .
   ```

2. Modele GGUF znajdują się w `/home/michal/Projects/LModels/GGUF`; domyślna
   konfiguracja wskazuje lokalną kopię Bielika. Aby użyć innego modelu, zmień
   ścieżkę w `config/models.yaml`.
3. Uruchom eksperyment:

   ```bash
   .venv/bin/ltt run
   ```

Każde uruchomienie zapisuje transcript JSON w `data/logs/` oraz metadane i tury
w `data/sqlite/let_them_talk.db`.

## Powtarzalne testy rozmów

Kompletny zestaw testowy jest w `dialogue_tests/`. Zawiera profile ról,
scenariusz, schemat ręcznej adnotacji metryk i skrypty do uruchomienia oraz
odczytu logów. Start: `./dialogue_tests/run_cpu_mixed.sh`.

Krótki test Bielika uruchomisz przez `ltt run --experiment bielik_smoke`.

## Ważne

Jeśli obaj agenci wskazują ten sam model, wczytywany jest tylko raz. To oszczędza
pamięć RAM. Zakończenie dyskusji następuje, gdy agent B użyje znacznika
`[KONIEC_DYSKUSJI]`; znacznik pozostaje w logu, więc warunek końca jest audytowalny.
