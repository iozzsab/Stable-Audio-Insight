**Idioma:**
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

## Inicio rápido

0. [Download Last Release](https://github.com/oscarlumiere/Stable-Audio-Insight/releases/latest)
1. Regístrese en https://huggingface.co (omita si ya tiene cuenta)
2. Abra https://huggingface.co/stabilityai/stable-audio-open-1.0 → haga clic en **Agree and access repository**
3. En https://huggingface.co/settings/tokens → **New token** → Type: Read → Create
4. Ejecute `install.bat` → elija el idioma → pegue el token → elija el traductor. Listo.

Luego `run.bat` abre http://127.0.0.1:7860.


Aplicación Windows autocontenida para [Stable Audio Open 1.0](https://huggingface.co/stabilityai/stable-audio-open-1.0) de Stability AI. Pensada para diseño sonoro, audio de juegos, edición de vídeo y bocetos musicales.

## Qué incluye

- **UI en 9 idiomas** (English, Русский, 中文, 日本語, Español, Français, Deutsch, Português, 한국어) — el conmutador del pie de página de Gradio cambia todo al vuelo
- **Prompts multilingües** — escriba en cirílico / CJK / árabe / hebreo / griego / tailandés / devanagari, traducción automática al inglés antes de generar. Dos opciones en la instalación: `opus-mt-mul-en` (light, ~300 MB) o `nllb-200-distilled-600M` (heavy, ~2.4 GB)
- **~217 presets en 15 categorías** — Pasos, Impactos, Movimiento, UI, Armas, Ambiente, Vehículos, Naturaleza, Música, Cinemático, Magia, Sci-Fi, Horror, Animales, Multitud y voz
- **Generación multi-variación** — 1 a 4 audios por clic (`num_waveforms_per_prompt`), selector de scheduler (Default / DPM++ 2M / Euler), botón de seed aleatorio, botón Re-roll
- **Historial de sesión** — últimas 10 generaciones como mini-reproductores plegables
- **Modo batch** — pegue varios prompts (uno por línea), cada uno guardado directamente en `outputs/Saved/`
- **Exportar ZIP** de `outputs/Saved/` con un clic
- **Salida game-ready** — nombres de archivo slug (`wood_floor_footsteps_01.wav`) con contador por carpeta; metadatos WAV INFO con prompt completo, seed, duración, steps, cfg, frecuencia, negative — leídos por Reaper, Audition, Ableton, ffprobe
- **Conmutador GPU/CPU en vivo** y `RunOnCPU.bat` para sistemas con poca VRAM
- **Log por sesión** en `logs/app-YYYYMMDD-HHMMSS.log` con trazas completas en errores
- **Instalador de un archivo** (`install.bat`) — instala Python 3.11.9 silenciosamente dentro del proyecto, elige `torch+cu128` o CPU torch según `nvidia-smi`, descarga el modelo y el traductor. Verdaderamente portátil: eliminar la carpeta no deja rastro
- **Actualización** — `update.bat` refresca dependencias y resincroniza modelos

## Requisitos

- Windows 10 / 11 (probado en Windows 11 Pro)
- Python **3.11.x** — https://www.python.org/downloads/release/python-3119/
  (durante la instalación marque **Add Python to PATH**)
- GPU NVIDIA con CUDA 12.x:
  - **Mínimo**: ~4 GB VRAM (fp16, 1 variación, ≤ 20 s, ≤ 100 pasos)
  - **Recomendado**: 8 GB+ VRAM para 4 variaciones × 47 s con 100+ pasos
  - 6 GB funciona bien con 1–2 variaciones; 4 simultáneas pueden causar OOM
  - Para otras versiones de CUDA cambie el índice de PyTorch en
    `install.bat` / `setup.bat` (p.ej. `cu121` para CUDA 12.1)
  - Sin NVIDIA → use `RunOnCPU.bat` o el conmutador **GPU/CPU** de la
    interfaz (más lento, pero funciona)
- **15–20 GB libres durante la instalación** (después: ~10–13 GB residentes):
  - ~5 GB — pesos de Stable Audio Open
  - ~4–5 GB — Python + PyTorch CUDA + dependencias
  - 0.3–2.4 GB — traductor (según elección)
  - ~5 GB — cachés de HuggingFace y pip + archivos temporales de instalación (mayormente recuperables después)
- Cuenta de HuggingFace + token de lectura (solo para la descarga inicial)

## ¿Necesito un token de HuggingFace?

**Una sola vez — solo para descargar los pesos de Stable Audio.** Después la
aplicación funciona sin conexión desde el caché local `hf-cache/`.

Stable Audio Open 1.0 es un modelo *gated* — Stability AI exige cuenta
registrada y aceptación de la licencia antes de descargar. Por lo tanto:

1. Regístrese en https://huggingface.co (si aún no lo está)
2. Abra la página del modelo y **acepte la licencia**:
   https://huggingface.co/stabilityai/stable-audio-open-1.0
   (haga clic en **Agree and access repository** — sin esto la descarga
   devuelve 403)
3. Cree un token de lectura: https://huggingface.co/settings/tokens
4. `install.bat` le pedirá el token en el momento adecuado

Los traductores (`opus-mt-mul-en` y `nllb-200-distilled-600M`) **no**
requieren token — son modelos públicos.

## Instalación (recomendada)

Un solo archivo hace todo:

```
install.bat
```

Pasos:

1. Elige el idioma de los prompts (1–9: inglés, ruso, chino, japonés,
   español, francés, alemán, portugués, coreano)
2. Verifica que Python 3.11 esté en PATH (`py -3.11`)
3. Crea `.venv` y actualiza pip / wheel
4. Instala PyTorch (CUDA 12.8) y el resto de `requirements.txt`
5. Pide el token HF (o lo omite si ya inició sesión)
6. **Pregunta qué traductor instalar:**
   - **1. LIGHT** — `Helsinki-NLP/opus-mt-mul-en`
     - ~300 MB, rápido, Apache 2.0 (uso comercial permitido)
     - Calidad media, a veces falla con términos musicales
   - **2. HEAVY** — `facebook/nllb-200-distilled-600M`
     - ~2.4 GB, más lento, CC-BY-NC 4.0 (**solo no comercial**)
     - Mayor calidad, recomendado para idiomas no ingleses
7. Guarda la elección en `hf-cache/translator.cfg`
8. Descarga Stable Audio (~5 GB) y el traductor elegido en `hf-cache/`

## Ejecución

```
run.bat
```

Se abre una pestaña en http://127.0.0.1:7860.

## Cambiar traductor tras la instalación

Forma rápida:

1. Abra `hf-cache/translator.cfg` y cambie a `light` o `heavy`
2. Ejecute `download.bat` — descargará el elegido si falta en caché
3. `run.bat`

O elimine `hf-cache/translator.cfg` y ejecute `install.bat` de nuevo — preguntará otra
vez y no volverá a descargar dependencias ni Stable Audio (ya en caché).

## Instalación paso a paso (si algo falla)

`install.bat` envuelve cuatro scripts que se pueden ejecutar por separado:

| Script | Función |
| --- | --- |
| `setup.bat` | Crea `.venv` e instala dependencias |
| `login.bat` | Autenticación HuggingFace (`hf auth login`) |
| `download.bat` | Descarga Stable Audio + traductor desde `hf-cache/translator.cfg` |
| `run.bat` | Inicia la UI web Gradio |

## Estructura del proyecto

```
.
├── app.py              # UI Gradio + generación
├── translator.py       # Módulo de traducción (light / heavy)
├── download_model.py   # Descarga de modelos desde HuggingFace
├── requirements.txt    # Dependencias Python
├── install.bat         # Instalador único (multilingüe)
├── setup.bat           # Solo venv + dependencias
├── login.bat           # Solo autenticación HF
├── download.bat        # Solo descarga
├── run.bat             # Inicia la UI web
├── hf-cache/translator.cfg  # light / heavy (creado por install.bat)
├── README.md           # main docs (English)
├── docs/i18n/          # localized versions (8 languages)
├── LICENSE             # MIT — código fuente
├── NOTICE.md           # Licencias de los modelos usados
├── hf-cache/           # Caché HF local (NO en git)
└── outputs/            # Audio guardado (NO en git)
    ├── intermediate/   # Casilla "Save all" activa
    └── Saved/          # Tras pulsar "Save"
```

## Variables de entorno

Se pueden definir antes de `run.bat`:

| Variable | Defecto | Uso |
| --- | --- | --- |
| `HOST` | `127.0.0.1` | Host Gradio |
| `PORT` | `7860` | Puerto Gradio |
| `SHARE` | `0` | `1` = crear enlace público gradio.live |
| `STABLE_AUDIO_MODEL` | `stabilityai/stable-audio-open-1.0` | Modelo alterno |

## Licencias

Este **código fuente** es MIT (ver `LICENSE`).

Los **modelos** tienen licencias propias (texto completo en `NOTICE.md`):

| Modelo | Licencia | Uso comercial |
| --- | --- | --- |
| Stable Audio Open 1.0 | Stability AI Community | Hasta $1M anual: sí; por encima: licencia Enterprise |
| opus-mt-mul-en (light) | Apache 2.0 | Sí |
| NLLB-200-distilled-600M (heavy) | CC-BY-NC 4.0 | **No, solo no comercial** |

Para uso comercial, elija el traductor **light** durante la instalación.

## Probado en

- Windows 11 Pro
- Python 3.11.9
- NVIDIA RTX 5080 (16 GB VRAM)
- CUDA 12.8
- PyTorch 2.11.0+cu128

## Créditos

- **[Stable Audio Open 1.0](https://huggingface.co/stabilityai/stable-audio-open-1.0)** — Stability AI
- **[opus-mt-mul-en](https://huggingface.co/Helsinki-NLP/opus-mt-mul-en)** — Helsinki-NLP / Tatoeba Translation Challenge
- **[NLLB-200](https://huggingface.co/facebook/nllb-200-distilled-600M)** — Meta AI / FAIR
- **[Gradio](https://github.com/gradio-app/gradio)**, **[diffusers](https://github.com/huggingface/diffusers)**, **[transformers](https://github.com/huggingface/transformers)**, **[accelerate](https://github.com/huggingface/accelerate)** — HuggingFace
- **Desarrollo del wrapper** — [Oscar Lumiere](https://www.io-oscar.com/)
- **Asistencia** — [Claude Code](https://www.anthropic.com/claude-code) (Anthropic)
