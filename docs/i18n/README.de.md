**Sprache:**
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

## Schnellstart

0. [Download Last Release](https://github.com/oscarlumiere/Stable-Audio-Insight/releases/latest)
1. Registrieren auf https://huggingface.co (überspringen, wenn Konto vorhanden)
2. Öffnen Sie https://huggingface.co/stabilityai/stable-audio-open-1.0 → klicken Sie auf **Agree and access repository**
3. Auf https://huggingface.co/settings/tokens → **New token** → Type: Read → Create
4. `install.bat` starten → Sprache wählen → Token einfügen → Übersetzer wählen. Fertig.

Danach öffnet `run.bat` http://127.0.0.1:7860.


Eigenständige Windows-App für [Stable Audio Open 1.0](https://huggingface.co/stabilityai/stable-audio-open-1.0) von Stability AI. Konzipiert für Sounddesign, Spiele-Audio, Videobearbeitung und Musikskizzen.

## Funktionen

- **UI in 9 Sprachen** (English, Русский, 中文, 日本語, Español, Français, Deutsch, Português, 한국어) — Umschalter in der Gradio-Fußzeile wechselt alles in Echtzeit
- **Mehrsprachige Prompts** — Eingabe in Kyrillisch / CJK / Arabisch / Hebräisch / Griechisch / Thai / Devanagari, automatische Übersetzung ins Englische vor der Generierung. Zwei Optionen bei der Installation: `opus-mt-mul-en` (light, ~300 MB) oder `nllb-200-distilled-600M` (heavy, ~2,4 GB)
- **~217 Presets in 15 Kategorien** — Schritte, Treffer, Bewegung, UI, Waffen, Ambiente, Fahrzeuge, Natur, Musik, Cinematic, Magie, Sci-Fi, Horror, Tiere, Menge und Stimmen
- **Multi-Variationen-Generierung** — 1 bis 4 Audios pro Klick (`num_waveforms_per_prompt`), Scheduler-Auswahl (Default / DPM++ 2M / Euler), Zufalls-Seed-Button, Re-roll-Button
- **Sitzungsverlauf** — letzte 10 Generierungen als einklappbare Mini-Player
- **Batch-Modus** — mehrere Prompts (einer pro Zeile), jeder direkt in `outputs/Saved/` gespeichert
- **ZIP-Export** von `outputs/Saved/` mit einem Klick
- **Game-Ready-Ausgabe** — Slug-Dateinamen (`wood_floor_footsteps_01.wav`) mit ordnerbezogenem Zähler; WAV-INFO-Metadaten mit vollem Prompt, Seed, Dauer, Steps, CFG, Sample-Rate, Negative — lesbar von Reaper, Audition, Ableton, ffprobe
- **GPU/CPU-Live-Umschaltung** und `RunOnCPU.bat` für Systeme mit wenig VRAM
- **Sitzungsprotokoll** in `logs/app-YYYYMMDD-HHMMSS.log` mit vollständigen Tracebacks bei Fehlern
- **Ein-Datei-Installer** (`install.bat`) — installiert Python 3.11.9 still in den Projektordner, wählt `torch+cu128` oder CPU-Torch via `nvidia-smi`, lädt Modell und Übersetzer. Wirklich portabel: Ordner löschen hinterlässt keine Spuren
- **Update-Pfad** — `update.bat` aktualisiert Abhängigkeiten und synchronisiert Modelle neu

## Voraussetzungen

- Windows 10 / 11 (getestet auf Windows 11 Pro)
- Python **3.11.x** — https://www.python.org/downloads/release/python-3119/
  (während der Installation **Add Python to PATH** ankreuzen)
- NVIDIA-GPU mit CUDA 12.x:
  - **Minimum**: ~4 GB VRAM (fp16, 1 Variation, ≤ 20 s, ≤ 100 Schritte)
  - **Empfohlen**: 8 GB+ VRAM für 4 Variationen × 47 s mit 100+ Schritten
  - 6 GB reichen für 1–2 Variationen; 4 gleichzeitig können OOM auslösen
  - Für andere CUDA-Versionen den PyTorch-Index in `install.bat` /
    `setup.bat` anpassen (z. B. `cu121` für CUDA 12.1)
  - Keine NVIDIA → `RunOnCPU.bat` oder den **GPU/CPU**-Schalter im UI
    nutzen (langsamer, funktioniert aber)
- **15–20 GB freier Speicher während der Installation** (danach: ~10–13 GB resident):
  - ~5 GB — Stable-Audio-Open-Gewichte
  - ~4–5 GB — Python + PyTorch CUDA + Abhängigkeiten
  - 0,3–2,4 GB — Übersetzer (je nach Wahl)
  - ~5 GB — HuggingFace- und pip-Cache + Installations-Temp-Dateien (das meiste später löschbar)
- HuggingFace-Konto + Read-Token (nur für den Erst-Download)

## Brauche ich ein HuggingFace-Token?

**Einmalig — nur zum Herunterladen der Stable-Audio-Gewichte.** Danach läuft
die Anwendung offline aus dem lokalen `hf-cache/`.

Stable Audio Open 1.0 ist ein *gated* Modell — Stability AI verlangt ein
registriertes Konto und Lizenz-Zustimmung vor dem Download. Daher:

1. Registrieren Sie sich auf https://huggingface.co (falls noch nicht
   geschehen)
2. Öffnen Sie die Modell-Seite und **akzeptieren Sie die Lizenz**:
   https://huggingface.co/stabilityai/stable-audio-open-1.0
   (klicken Sie **Agree and access repository** — ohne dies gibt der
   Download 403 zurück)
3. Erstellen Sie ein Read-Token: https://huggingface.co/settings/tokens
4. `install.bat` fragt das Token zum richtigen Zeitpunkt ab

Die Übersetzer (`opus-mt-mul-en` und `nllb-200-distilled-600M`) benötigen
**kein** Token — sie sind öffentlich.

## Installation (empfohlener Weg)

Eine Datei macht alles:

```
install.bat
```

Was sie tut:

1. Sprache der Eingabeaufforderungen wählen (1–9: Englisch, Russisch,
   Chinesisch, Japanisch, Spanisch, Französisch, Deutsch, Portugiesisch,
   Koreanisch)
2. Prüft, ob Python 3.11 in PATH ist (`py -3.11`)
3. Erstellt `.venv`, aktualisiert pip / wheel
4. Installiert PyTorch (CUDA 12.8) und den Rest aus `requirements.txt`
5. Fragt nach dem HF-Token (oder überspringt, falls bereits angemeldet)
6. **Fragt, welcher Übersetzer installiert werden soll:**
   - **1. LIGHT** — `Helsinki-NLP/opus-mt-mul-en`
     - ~300 MB, schnell, Apache 2.0 (kommerziell erlaubt)
     - Mittlere Qualität, Musik-Begriffe manchmal falsch
   - **2. HEAVY** — `facebook/nllb-200-distilled-600M`
     - ~2,4 GB, langsamer, CC-BY-NC 4.0 (**nur nicht-kommerziell**)
     - Höhere Qualität, empfohlen für nicht-Englisch
7. Speichert die Wahl in `hf-cache/translator.cfg`
8. Lädt Stable Audio (~5 GB) und den gewählten Übersetzer nach `hf-cache/`

## Starten

```
run.bat
```

Ein Browser-Tab öffnet http://127.0.0.1:7860.

## Übersetzer nach der Installation wechseln

Schnellster Weg:

1. `hf-cache/translator.cfg` öffnen und auf `light` oder `heavy` ändern
2. `download.bat` ausführen — lädt das Gewählte, falls nicht im Cache
3. `run.bat`

Oder `hf-cache/translator.cfg` löschen und `install.bat` erneut ausführen — fragt
neu, ohne Abhängigkeiten oder Stable Audio erneut herunterzuladen
(bereits im Cache).

## Schritt-für-Schritt-Installation (falls etwas schiefgeht)

`install.bat` ist ein Wrapper für vier kleinere Skripte; jedes kann einzeln
ausgeführt werden:

| Skript | Funktion |
| --- | --- |
| `setup.bat` | Erstellt `.venv` und installiert Abhängigkeiten |
| `login.bat` | HuggingFace-Authentifizierung (`hf auth login`) |
| `download.bat` | Lädt Stable Audio + Übersetzer aus `hf-cache/translator.cfg` |
| `run.bat` | Startet die Gradio-Web-UI |

## Projekt-Struktur

```
.
├── app.py              # Gradio-UI + Generierung
├── translator.py       # Übersetzer-Modul (light / heavy)
├── download_model.py   # Modelldownloads von HuggingFace
├── requirements.txt    # Python-Abhängigkeiten
├── install.bat         # Ein-Klick-Installer (mehrsprachig)
├── setup.bat           # Nur venv + Abhängigkeiten
├── login.bat           # Nur HF-Auth
├── download.bat        # Nur Downloads
├── run.bat             # Web-UI starten
├── hf-cache/translator.cfg  # light / heavy (von install.bat erstellt)
├── README.md           # main docs (English)
├── docs/i18n/          # localized versions (8 languages)
├── LICENSE             # MIT — Quellcode des Repos
├── NOTICE.md           # Lizenzen der verwendeten Modelle
├── hf-cache/           # Lokaler HF-Cache (NICHT in git)
└── outputs/            # Gespeicherte Audios (NICHT in git)
    ├── intermediate/   # Wenn "Save all" aktiviert ist
    └── Saved/          # Nach Klick auf "Save"
```

## Umgebungsvariablen

Vor `run.bat` setzbar:

| Variable | Standard | Zweck |
| --- | --- | --- |
| `HOST` | `127.0.0.1` | Gradio-Host |
| `PORT` | `7860` | Gradio-Port |
| `SHARE` | `0` | `1` = öffentlichen gradio.live-Link erzeugen |
| `STABLE_AUDIO_MODEL` | `stabilityai/stable-audio-open-1.0` | Modell überschreiben |

## Lizenzen

Der **Quellcode** steht unter MIT (siehe `LICENSE`).

Die **Modelle** haben jeweils eigene Lizenzen (Volltexte in `NOTICE.md`):

| Modell | Lizenz | Kommerzielle Nutzung |
| --- | --- | --- |
| Stable Audio Open 1.0 | Stability AI Community | Bis 1 Mio. USD Jahresumsatz: ja; darüber: Enterprise |
| opus-mt-mul-en (light) | Apache 2.0 | Ja |
| NLLB-200-distilled-600M (heavy) | CC-BY-NC 4.0 | **Nein, nur nicht-kommerziell** |

Für kommerzielle Nutzung wählen Sie bei der Installation **light**.

## Getestet auf

- Windows 11 Pro
- Python 3.11.9
- NVIDIA RTX 5080 (16 GB VRAM)
- CUDA 12.8
- PyTorch 2.11.0+cu128

## Credits

- **[Stable Audio Open 1.0](https://huggingface.co/stabilityai/stable-audio-open-1.0)** — Stability AI
- **[opus-mt-mul-en](https://huggingface.co/Helsinki-NLP/opus-mt-mul-en)** — Helsinki-NLP / Tatoeba Translation Challenge
- **[NLLB-200](https://huggingface.co/facebook/nllb-200-distilled-600M)** — Meta AI / FAIR
- **[Gradio](https://github.com/gradio-app/gradio)**, **[diffusers](https://github.com/huggingface/diffusers)**, **[transformers](https://github.com/huggingface/transformers)**, **[accelerate](https://github.com/huggingface/accelerate)** — HuggingFace
- **Wrapper-Entwicklung** — [Oscar Lumiere](https://www.io-oscar.com/)
- **Unterstützung** — [Claude Code](https://www.anthropic.com/claude-code) (Anthropic)
