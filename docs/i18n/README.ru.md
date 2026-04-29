**Язык:**
[English](../../README.md) ·
[Русский](README.ru.md) ·
[中文](README.zh.md) ·
[日本語](README.ja.md) ·
[Español](README.es.md) ·
[Français](README.fr.md) ·
[Deutsch](README.de.md) ·
[Português](README.pt.md) ·
[한국어](README.ko.md)

---

# Stable Audio Insight

*By Oscar Lumiere*

## Быстрый старт

1. Зарегистрируйтесь на https://huggingface.co (пропустите, если уже есть аккаунт)
2. Откройте https://huggingface.co/stabilityai/stable-audio-open-1.0 → нажмите **Agree and access repository**
3. На https://huggingface.co/settings/tokens → **New token** → Type: Read → Create
4. Запустите `install.bat` → выберите язык → вставьте токен → выберите переводчик. Готово.

Потом `run.bat` откроет http://127.0.0.1:7860.


Self-contained Windows-приложение для [Stable Audio Open 1.0](https://huggingface.co/stabilityai/stable-audio-open-1.0) от Stability AI. Сделано для звукового дизайна, геймдева, видеомонтажа и музыкальных набросков.

## Что внутри

- **UI на 9 языках** (English, Русский, 中文, 日本語, Español, Français, Deutsch, Português, 한국어) — переключатель в футере Gradio меняет всё на лету
- **Мультиязычные промпты** — пишите кириллицей / CJK / арабским / ивритом / греческим / тайским / деванагари, автоматический перевод на английский перед генерацией. На выбор при установке: `opus-mt-mul-en` (light, ~300 МБ) или `nllb-200-distilled-600M` (heavy, ~2.4 ГБ)
- **~217 готовых пресетов в 15 категориях** — Шаги, Удары, Движение, UI, Оружие, Амбиент, Транспорт, Природа, Музыка, Кинематограф, Магия, Sci-Fi, Хоррор, Животные, Толпа/голоса
- **Мульти-вариация** — от 1 до 4 аудио за один клик (`num_waveforms_per_prompt`), выбор шедулера (Default / DPM++ 2M / Euler), кнопка случайного seed, кнопка Re-roll
- **История сессии** — последние 10 генераций мини-плеерами в аккордеоне
- **Batch-режим** — список промптов (по одному в строку), каждый сразу сохраняется в `outputs/Saved/`
- **ZIP-экспорт** `outputs/Saved/` одной кнопкой
- **Game-ready вывод** — slug-имена (`wood_floor_footsteps_01.wav`) со счётчиком по папке; в WAV INFO chunk пишется title (полный промпт), seed, длительность, steps, cfg, sample rate, negative — читают Reaper, Audition, Ableton, ffprobe
- **Переключение GPU/CPU** + `RunOnCPU.bat` для слабых VRAM-систем
- **Лог сессии** в `logs/app-YYYYMMDD-HHMMSS.log` с полными трейсбеками ошибок
- **Один установщик** (`install.bat`) — тихо ставит Python 3.11.9 внутрь папки проекта, авто-детект GPU (`torch+cu128` или CPU torch), качает модель и переводчик. Truly portable: удалили проект — в системе ноль следов
- **Обновление** — `update.bat` обновляет зависимости и пересинхронизирует модели

## Системные требования

- Windows 10 / 11 (тестировалось на Windows 11 Pro)
- Python **3.11.x** — https://www.python.org/downloads/release/python-3119/
  (при установке отметьте **Add Python to PATH**)
- NVIDIA GPU с CUDA 12.8 (тестировалось на RTX 5080, 16 ГБ VRAM).
  Для других серий замените индекс PyTorch в `install.bat` / `setup.bat`
  (например `cu121` для CUDA 12.1).
- **15–20 ГБ свободного места** на время установки (после: ~10–13 ГБ резидентно):
  - ~5 ГБ — веса Stable Audio Open
  - ~4–5 ГБ — Python + PyTorch CUDA + зависимости
  - 0.3–2.4 ГБ — переводчик (по выбору)
  - ~5 ГБ — кэши HuggingFace и pip + временные файлы установки (большую часть можно потом удалить)
- HuggingFace аккаунт + read-токен (нужен только при первой загрузке)

## HuggingFace-токен — нужен или нет?

**Нужен один раз — только для скачивания весов Stable Audio.** После этого
приложение работает офлайн из локального кэша `hf-cache/`.

Stable Audio Open 1.0 — *gated* модель: Stability AI требует зарегистрированный
аккаунт и принятие лицензии перед загрузкой. Поэтому:

1. Зарегистрируйтесь на https://huggingface.co (если ещё нет)
2. Откройте страницу модели и **примите лицензию**:
   https://huggingface.co/stabilityai/stable-audio-open-1.0
   (нажмите **Agree and access repository** — обязательно, иначе загрузка
   вернёт 403)
3. Создайте read-токен: https://huggingface.co/settings/tokens
4. `install.bat` попросит вставить токен в нужный момент

Для переводчиков (`opus-mt-mul-en` и `nllb-200-distilled-600M`) токен **не
требуется** — это публичные модели.

## Установка (рекомендуемый способ)

Один файл — всё ставится за раз:

```
install.bat
```

Что он делает:

1. Спрашивает язык подсказок (1–9: английский, русский, китайский, японский,
   испанский, французский, немецкий, португальский, корейский)
2. Проверяет Python 3.11 в PATH (`py -3.11`)
3. Создаёт `.venv` и обновляет pip / wheel
4. Ставит PyTorch (CUDA 12.8) и остальное из `requirements.txt`
5. Просит HF-токен (или пропускает, если уже логинились)
6. **Спрашивает, какой переводчик ставить:**
   - **1. LIGHT** — `Helsinki-NLP/opus-mt-mul-en`
     - ~300 МБ, быстрый, Apache 2.0 (можно коммерчески)
     - Среднее качество, иногда ошибается на музыкальных терминах
   - **2. HEAVY** — `facebook/nllb-200-distilled-600M`
     - ~2.4 ГБ, медленнее, CC-BY-NC 4.0 (**только некоммерческое**)
     - Более качественный, рекомендуется для русского
7. Сохраняет выбор в `hf-cache/translator.cfg`
8. Скачивает Stable Audio (~5 ГБ) и выбранный переводчик в `hf-cache/`

## Запуск

```
run.bat
```

В браузере откроется http://127.0.0.1:7860.

## Сменить переводчик после установки

Самый простой путь:

1. Откройте `hf-cache/translator.cfg`, поменяйте на `light` или `heavy`
2. Запустите `download.bat` — скачает выбранный, если ещё нет в кэше
3. `run.bat`

Или удалите `hf-cache/translator.cfg` и запустите `install.bat` снова — он спросит
заново и не докачает повторно зависимости и Stable Audio (уже в кэше).

## Установка по шагам (если что-то пошло не так)

`install.bat` — это связка из четырёх отдельных скриптов, любой можно
запустить отдельно:

| Файл | Что делает |
| --- | --- |
| `setup.bat` | Создаёт `.venv` и ставит зависимости |
| `login.bat` | HuggingFace-авторизация (`hf auth login`) |
| `download.bat` | Скачивание Stable Audio + переводчика из `hf-cache/translator.cfg` |
| `run.bat` | Запуск Gradio веб-интерфейса |

## Структура проекта

```
.
├── app.py              # Gradio UI + генерация
├── translator.py       # Модуль переводчика (light / heavy)
├── download_model.py   # Загрузка моделей с HuggingFace
├── requirements.txt    # Python-зависимости
├── install.bat         # Единый установщик (многоязычный)
├── setup.bat           # Только venv + зависимости
├── login.bat           # Только HF-авторизация
├── download.bat        # Только загрузка моделей
├── run.bat             # Запуск веб-интерфейса
├── hf-cache/translator.cfg  # light / heavy (создаётся install.bat)
├── README.md           # main docs (English)
├── docs/i18n/          # localized versions (8 languages)
├── LICENSE             # MIT — для кода в этом репозитории
├── NOTICE.md           # Лицензии используемых моделей
├── hf-cache/           # Локальный кэш HF (НЕ в git)
└── outputs/            # Сохранённое аудио (НЕ в git)
    ├── intermediate/   # При включённом чекбоксе «Save all»
    └── Saved/          # При нажатии кнопки «Save»
```

## Переменные окружения

Можно настроить перед запуском `run.bat`:

| Переменная | По умолчанию | Назначение |
| --- | --- | --- |
| `HOST` | `127.0.0.1` | Хост Gradio |
| `PORT` | `7860` | Порт Gradio |
| `SHARE` | `0` | `1` — создать публичную ссылку gradio.live |
| `STABLE_AUDIO_MODEL` | `stabilityai/stable-audio-open-1.0` | Переопределить модель |

## Лицензии

**Код** — MIT (см. `LICENSE`).

**Модели** — каждая со своей лицензией (полные тексты в `NOTICE.md`):

| Модель | Лицензия | Коммерческое использование |
| --- | --- | --- |
| Stable Audio Open 1.0 | Stability AI Community | До $1M годовой выручки — да; выше — Enterprise |
| opus-mt-mul-en (light) | Apache 2.0 | Да |
| NLLB-200-distilled-600M (heavy) | CC-BY-NC 4.0 | **Нет, только некоммерческое** |

Если планируете коммерческое использование — выбирайте при установке
**light**-переводчик.

## Тестировалось на

- Windows 11 Pro
- Python 3.11.9
- NVIDIA RTX 5080 (16 ГБ VRAM)
- CUDA 12.8
- PyTorch 2.11.0+cu128

## Credits

- **Stable Audio Open 1.0** — Stability AI
- **opus-mt-mul-en** — Helsinki-NLP / Tatoeba Translation Challenge
- **NLLB-200** — Meta AI / FAIR
- **Gradio**, **diffusers**, **transformers**, **accelerate** — HuggingFace
- **Разработка обёртки** — Oscar Lumiere
- **Помощь** — [Claude Code](https://www.anthropic.com/claude-code) (Anthropic)
