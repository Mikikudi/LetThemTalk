# LetThemTalk

Lokalna platforma do prowadzenia eksperymentów z dyskusją dwóch lub więcej modeli językowych działających lokalnie na Arch Linux. Projekt ma na celu badanie wpływu różnych profili tuningowych, system promptów i konfiguracji runtime na zachowania modeli w rozmowie, przy minimalnym koszcie abstrakcji i maksymalnej przejrzystości środowiska eksperymentalnego.

## Cel projektu

- uruchamianie lokalnych LM-ów bez zewnętrznych API,
- testowanie wielu agentów o różnych profilach zachowań,
- zapis każdej rozmowy jako danych badawczych,
- łatwa integracja z `llama.cpp` oraz z lokalnymi konfiguracjami modeli `FastFlowLM` / `FLM` i `Ryzen AI` przygotowanymi pod środowiska AMD,
- utrzymanie prostego, czytelnego i mało abstrakcyjnego modelu architektury.

## Główne technologie

- `llama.cpp` / `llama-cpp-python` — warstwa inferencji i ładowania modeli GGUF lokalnie,
- `FastFlowLM` / `FLM` — oznaczenia plików wag i konfiguracji modeli przygotowanych pod ekosystem AMD, używanych jako lokalne artefakty modelowe w eksperymentach,
- `Ryzen AI` — etykieta konfiguracji i zestawów wag przygotowanych pod procesory i układy AMD, wspierających lokalne uruchamianie modeli bez zewnętrznego API,
- Python 3.12+ — orchestracja agentów i logowanie,
- SQLite — zapis eksperymentów i rozmów,
- YAML/JSON — konfiguracja modeli, promptów i eksperymentów,
- opcjonalnie: `pandas`, `matplotlib`, `jupyter` do analizy wyników.

## Założenia architektoniczne

Projekt ma być prosty i transparentny:

- brak dużego frameworku aplikacyjnego,
- brak niepotrzebnej warstwy backendowej,
- każda rozmowa jest zapisywana jako obiekt eksperymentu,
- każda instancja modelu ma jawnie zdefiniowany profil: model, tuning, prompt, config runtime,
- agent ma jasno określone zachowanie, a nie tylko „losowy” prompt.

## Struktura projektu

```text
LetThemTalk/
├── README.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── config/
│   ├── agents.yaml
│   ├── models.yaml
│   ├── experiments.yaml
│   └── prompts/
│       ├── persona_a.txt
│       ├── persona_b.txt
│       └── task_prompt.txt
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── model_runtime.py
│   ├── agent.py
│   ├── conversation.py
│   ├── storage.py
│   ├── logger.py
│   ├── cli.py
│   └── analysis.py
├── scripts/
│   ├── run_experiment.py
│   ├── run_local_chat.py
│   ├── export_logs.py
│   ├── benchmark_models.py
│   └── fastflowlm/
│       ├── prepare_models.py
│       ├── convert_to_gguf.py
│       ├── benchmark_run.py
│       ├── eval_prompt_batch.py
│       └── run_fastflowlm_pipeline.py
├── data/
│   ├── models/
│   │   ├── gguf/
│   │   └── adapters/
│   ├── logs/
│   │   ├── conversations/
│   │   └── experiments/
│   └── sqlite/
│       └── let_they_talk.db
├── notebooks/
│   └── experiment_analysis.ipynb
└── tests/
    ├── test_conversation.py
    ├── test_storage.py
    └── test_config.py
```

## Rola warstw

### 1. `llama.cpp`

Służy jako podstawowy backend inferencji lokalnego:

- ładowanie modeli GGUF,
- uruchamianie lokalnych wywołań modelu,
- kontrola `n_ctx`, `n_gpu_layers`, `n_threads`, `temperature`, `max_tokens`,
- zapewnienie niskiego narzutu i maksymalnej wydajności na Arch Linux.

### 2. `FastFlowLM` / `FLM`

`FastFlowLM` i `FLM` to nie są osobne frameworki runtime, lecz nazwy wariantów i zestawów plików wag oraz konfiguracji modelowych zoptymalizowanych pod środowiska AMD. W praktyce mogą być wykorzystywane jako:

- gotowe konfiguracje modeli do lokalnego uruchomienia,
- zestawy wag przygotowanych pod architekturę AMD / Ryzen AI,
- artefakty eksperymentalne wspierające benchmarki i testy promptów,
- elementy pipeline do porównania wydajności w różnych profilach tuningowych.

W praktyce `FastFlowLM` / `FLM` nie zastępuje `llama.cpp`, lecz współdziała z nim jako źródło modelu i konfiguracji pod konkretne środowisko sprzętowe.

### 3. `src/`

Kod aplikacji odpowiedzialny za:

- konfigurację modeli i agentów,
- obsługę runtime i promptów,
- pętlę dyskusji między agentami,
- zapis historii do bazy danych,
- export logów i analitykę.

## Przykładowy model działania

1. Wczytanie konfiguracji eksperymentu z YAML.
2. Inicjalizacja modeli lokalnych przez `llama.cpp`.
3. Utworzenie agentów z różnymi promptami i profilami tuningowymi.
4. Rozpoczęcie rozmowy według zdefiniowanego scenariusza.
5. Zapis każdego kroku do SQLite.
6. Eksport danych do CSV/JSON lub notebooku do analizy.

## Zalecany scenariusz eksperymentu

Każdy eksperyment powinien rejestrować:

- identyfikator eksperymentu,
- datę i czas uruchomienia,
- nazwy modeli,
- ścieżki do plików GGUF,
- profile tuningowe,
- system prompty,
- temperaturę i parametry generacji,
- odpowiedzi poszczególnych agentów,
- metadane środowiska (Arch, CPU/GPU, liczba rdzeni, rozmiar kontekstu).

To pozwala na porównanie nie tylko treści odpowiedzi, ale również wpływu konfiguracji wykonania.

## Minimalna funkcjonalność MVP

W pierwszej wersji projekt powinien umożliwiać:

- uruchomienie 2–4 lokalnych agentów,
- wybór modeli z katalogu `data/models`,
- zdefiniowanie system promptów dla każdej roli,
- przeprowadzenie rozmowy w pętli,
- zapis wyników do SQLite,
- prosty eksport do `JSON` lub `CSV`.

## Dalsze kroki

Po wdrożeniu MVP można dodać:

- TUI do monitorowania aktywnej dyskusji,
- eksport eksperymentów do notebooków,
- metryki jakości dyskusji,
- automatyczne porównanie różnych profili tuningowych,
- integrację z dodatkowym zestawem konfiguracji i skryptów `FastFlowLM` / `FLM` / `Ryzen AI` dla AMD.

## Podsumowanie

To repozytorium ma być małym, lokalnym laboratorium do badania interakcji między modelami. Główny nacisk leży na:

- przejrzystość,
- niski koszt abstrakcji,
- kontrolę nad promptami i tuningiem,
- zachowanie wszystkich danych eksperymentalnych w sposób porównywalny i łatwy do analizy.

Projekt jest z założenia prosty, zorientowany na badania a nie na „produktową” warstwę frontendową.
