import logging
import os
import re
import shutil
import sys
import tempfile
import time
import zipfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)
_log_path = LOG_DIR / f"app-{time.strftime('%Y%m%d-%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(_log_path, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("app")
log.info(f"log file: {_log_path}")

import torch
import gradio as gr
from diffusers import StableAudioPipeline

from translator import Translator, needs_translation, get_kind, get_model_id
from i18n import TRANSLATIONS
from presets import PRESETS
from audio_io import slugify_prompt, next_counter, post_audio, write_wav_with_metadata

os.environ.setdefault("HF_HOME", str(ROOT / "hf-cache"))

MODEL_ID = os.environ.get("STABLE_AUDIO_MODEL", "stabilityai/stable-audio-open-1.0")
TMP_DIR = Path(tempfile.gettempdir()) / "stable-audio-open"
TMP_DIR.mkdir(exist_ok=True)
OUTPUTS_ROOT = ROOT / "outputs"
INTERMEDIATE_DIR = OUTPUTS_ROOT / "intermediate"
SAVED_DIR = OUTPUTS_ROOT / "Saved"

_force_device = os.environ.get("FORCE_DEVICE", "").lower()
if _force_device == "cpu":
    device = "cpu"
elif _force_device == "cuda":
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device != "cuda":
        log.warning("FORCE_DEVICE=cuda but CUDA unavailable — falling back to cpu")
else:
    device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32

log.info(f"device={device} dtype={dtype} model={MODEL_ID}" + (f" (forced via FORCE_DEVICE={_force_device})" if _force_device else ""))
log.info(f"HF cache: {os.environ['HF_HOME']}")

if device == "cuda":
    log.info(f"GPU: {torch.cuda.get_device_name(0)} ({torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB)")
else:
    log.warning("no CUDA device — running on CPU (slow)")

log.info("loading pipeline (first launch downloads ~5 GB)...")
try:
    pipe = StableAudioPipeline.from_pretrained(MODEL_ID, torch_dtype=dtype)
    pipe = pipe.to(device)
except Exception:
    log.exception("failed to load Stable Audio pipeline")
    raise
log.info("pipeline ready")

SAMPLE_RATE = pipe.vae.config.sampling_rate if hasattr(pipe.vae, "config") else 44100
MAX_DURATION = 47.0
MAX_VARIATIONS = 4
HISTORY_SIZE = 10

_original_scheduler = pipe.scheduler
SCHEDULERS = ["Default", "DPM++ 2M", "Euler"]


def set_scheduler(name: str) -> str:
    try:
        if name == "DPM++ 2M":
            from diffusers import DPMSolverMultistepScheduler
            pipe.scheduler = DPMSolverMultistepScheduler.from_config(_original_scheduler.config)
        elif name == "Euler":
            from diffusers import EulerDiscreteScheduler
            pipe.scheduler = EulerDiscreteScheduler.from_config(_original_scheduler.config)
        else:
            pipe.scheduler = _original_scheduler
        return f"Scheduler set to: {name}"
    except Exception as e:
        pipe.scheduler = _original_scheduler
        return f"Scheduler swap failed ({e}); reverted to default"

_translator = Translator()
log.info(f"translator: kind={get_kind()} model={get_model_id()}")


def set_device(choice: str) -> str:
    target = "cuda" if (choice == "GPU" and torch.cuda.is_available()) else "cpu"
    cur = str(pipe.device).split(":")[0]
    if cur == target:
        return f"Already on {target}"
    log.info(f"moving pipeline to {target}...")
    try:
        pipe.to(target)
        log.info(f"pipeline now on {target}")
        return f"Switched to {target} (slower on CPU)"
    except Exception as e:
        log.exception("device switch failed")
        return f"Device switch failed: {e}"


def live_translate(text: str) -> str:
    if not needs_translation(text):
        return ""
    try:
        return _translator.translate(text)
    except Exception as e:
        return f"[translation error: {e}]"


def live_translate_batch(text: str) -> str:
    if not text or not text.strip():
        return ""
    out_lines: list[str] = []
    any_translated = False
    for line in text.splitlines():
        if needs_translation(line):
            try:
                out_lines.append(_translator.translate(line))
                any_translated = True
            except Exception as e:
                out_lines.append(f"[translation error: {e}]")
                any_translated = True
        else:
            out_lines.append(line)
    if not any_translated:
        return ""
    return "\n".join(out_lines)


def _free_cuda():
    if str(pipe.device).startswith("cuda"):
        try:
            torch.cuda.empty_cache()
        except Exception:
            pass


def _append_log(new_msg: str, current_log_text: str) -> str:
    if new_msg is None:
        return current_log_text or ""
    msg = str(new_msg).strip()
    if not msg:
        return current_log_text or ""
    ts = time.strftime("%H:%M:%S")
    block = "\n".join(f"[{ts}] {line}" if i == 0 else f"           {line}"
                      for i, line in enumerate(msg.splitlines())) or f"[{ts}] {msg}"
    return f"{block}\n{current_log_text}" if current_log_text else block


def _empty_slot_updates() -> list:
    return [gr.update(value=None, visible=(i == 0)) for i in range(MAX_VARIATIONS)]


def _mini_audio_html(file_path: str | None, label: str) -> str:
    if not file_path:
        return ""
    from urllib.parse import quote
    url_path = quote(str(file_path).replace("\\", "/"))
    safe_label = (label or "").replace("<", "&lt;").replace(">", "&gt;")
    return (
        f'<div class="mini-track">'
        f'<div class="mini-label">{safe_label}</div>'
        f'<audio controls preload="none" style="width:100%;height:32px">'
        f'<source src="/gradio_api/file={url_path}">'
        f'</audio></div>'
    )


def _slot_updates(audio_paths: list[str | None], variations_count: int):
    updates = []
    for i in range(MAX_VARIATIONS):
        if i < variations_count and audio_paths[i]:
            updates.append(gr.update(value=audio_paths[i], visible=True))
        else:
            updates.append(gr.update(value=None, visible=False))
    return updates


def clear_audio_slots(variations_value):
    n = int(min(max(variations_value or 1, 1), MAX_VARIATIONS))
    return [gr.update(value=None, visible=(i < n)) for i in range(MAX_VARIATIONS)]


def generate(prompt: str, negative: str, seconds: float, steps: int, cfg: float, seed: int, save_all: bool, variations: int, progress=gr.Progress(track_tqdm=True)):
    if not prompt or not prompt.strip():
        gr.Warning("Enter a prompt")
        return (*_empty_slot_updates(), "ERROR: empty prompt")
    try:
        if needs_translation(prompt):
            prompt = _translator.translate(prompt)
        if needs_translation(negative):
            negative = _translator.translate(negative)

        seconds = float(min(max(seconds, 1.0), MAX_DURATION))
        steps = int(steps)
        cfg = float(cfg)
        seed = int(seed)
        variations = int(min(max(variations, 1), MAX_VARIATIONS))

        if seed < 0:
            seed = int(torch.randint(0, 2**31 - 1, (1,)).item())
        generator = torch.Generator(device=str(pipe.device).split(":")[0]).manual_seed(seed)

        log.info(f"gen prompt='{prompt[:80]}' dur={seconds}s steps={steps} cfg={cfg} seed={seed} variations={variations}")
        t0 = time.time()

        _free_cuda()

        def _do_pipe(s):
            return pipe(
                prompt=prompt,
                negative_prompt=negative or None,
                num_inference_steps=s,
                audio_end_in_s=seconds,
                guidance_scale=cfg,
                generator=generator,
                num_waveforms_per_prompt=variations,
            )

        try:
            result = _do_pipe(steps)
        except IndexError as ie:
            if "out of bounds" in str(ie).lower():
                log.warning(f"diffusers scheduler IndexError at steps={steps}; retrying with steps={steps+2}")
                _free_cuda()
                generator = torch.Generator(device=str(pipe.device).split(":")[0]).manual_seed(seed)
                result = _do_pipe(steps + 2)
                steps += 2
            else:
                raise

        slug = slugify_prompt(prompt)
        audio_paths: list[str | None] = [None] * MAX_VARIATIONS
        written_names: list[str] = []
        for i in range(variations):
            audio = post_audio(result.audios[i])
            counter = next_counter(TMP_DIR, slug)
            fname = TMP_DIR / f"{slug}_{counter:02d}.wav"
            metadata = {
                "title": prompt,
                "artist": "Stable Audio Insight",
                "software": f"Stable Audio Open 1.0 / {get_model_id()}",
                "creation_date": time.strftime("%Y-%m-%d"),
                "comment": (
                    f"seed={seed}; variation={i+1}/{variations}; duration={seconds:.1f}s; "
                    f"steps={steps}; cfg={cfg}; sample_rate={SAMPLE_RATE}Hz; "
                    f"negative={negative or ''}"
                ),
            }
            write_wav_with_metadata(fname, audio, SAMPLE_RATE, metadata)
            audio_paths[i] = str(fname)
            written_names.append(fname.name)
            if save_all:
                INTERMEDIATE_DIR.mkdir(parents=True, exist_ok=True)
                ic = next_counter(INTERMEDIATE_DIR, slug)
                shutil.copy2(fname, INTERMEDIATE_DIR / f"{slug}_{ic:02d}.wav")

        del result
        _free_cuda()

        elapsed = time.time() - t0
        info = f"seed={seed} | {seconds:.1f}s @ {SAMPLE_RATE} Hz | {steps} steps | {variations} var(s) | {elapsed:.1f}s gen"
        info += "\n" + ", ".join(written_names)
        if save_all:
            info += "\n-> copies in outputs/intermediate/"
        log.info(f"gen done: {info}")
        return (*_slot_updates(audio_paths, variations), info)
    except torch.cuda.OutOfMemoryError as e:
        _free_cuda()
        log.exception("CUDA out of memory")
        gr.Warning("CUDA out of memory — try fewer variations or shorter duration")
        return (*_empty_slot_updates(), f"ERROR: CUDA OOM — {e}")
    except KeyboardInterrupt:
        _free_cuda()
        log.info("generate() cancelled")
        raise
    except Exception as e:
        _free_cuda()
        log.exception("generate() failed")
        gr.Warning(f"Generation failed: {e}")
        return (*_empty_slot_updates(), f"ERROR: {e} (see log file for full traceback)")


MAX_BATCH_PREVIEW = 20


def generate_batch(batch_prompts: str, negative: str, seconds: float, steps: int, cfg: float, all_at_once: bool = False, save_all: bool = False, progress=gr.Progress(track_tqdm=True)):
    mode = "all" if all_at_once else "one"
    target_dir = SAVED_DIR if save_all else INTERMEDIATE_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    empty_previews = [gr.update(value="", visible=False) for _ in range(MAX_BATCH_PREVIEW)]
    if not batch_prompts or not batch_prompts.strip():
        yield ("Empty batch — paste prompts (one per line).", *empty_previews)
        return
    lines = [s.strip() for s in batch_prompts.splitlines() if s.strip()]
    if not lines:
        yield ("Empty batch — paste prompts (one per line).", *empty_previews)
        return

    n_eff = _translator.translate(negative) if needs_translation(negative) else (negative or "")
    seconds = float(min(max(seconds, 1.0), MAX_DURATION))
    steps = int(steps)
    cfg = float(cfg)
    results: list[str] = []
    previews = list(empty_previews)

    if mode == "all":
        yield (f"Translating {len(lines)} prompt(s)…", *previews)
        p_eff_list = [_translator.translate(p) if needs_translation(p) else p for p in lines]
        seeds = [int(torch.randint(0, 2**31 - 1, (1,)).item()) for _ in lines]
        device_str = str(pipe.device).split(":")[0]
        gens = [torch.Generator(device=device_str).manual_seed(s) for s in seeds]
        log.info(f"batch all-at-once: {len(lines)} prompts, single GPU pass, steps={steps}")
        yield (f"Running {len(lines)} prompt(s) in a single GPU pass…", *previews)
        _free_cuda()

        def _do_all(s):
            return pipe(
                prompt=p_eff_list,
                negative_prompt=[n_eff or ""] * len(lines) if n_eff else None,
                num_inference_steps=s,
                audio_end_in_s=seconds,
                guidance_scale=cfg,
                generator=gens,
            )

        try:
            try:
                res = _do_all(steps)
            except IndexError as ie:
                if "out of bounds" in str(ie).lower():
                    log.warning(f"batch-all: scheduler IndexError; retrying with steps={steps+2}")
                    _free_cuda()
                    gens = [torch.Generator(device=device_str).manual_seed(s) for s in seeds]
                    res = _do_all(steps + 2)
                else:
                    raise

            for i, audio_tensor in enumerate(res.audios, start=1):
                try:
                    audio = post_audio(audio_tensor)
                    slug = slugify_prompt(p_eff_list[i - 1])
                    counter = next_counter(target_dir, slug)
                    fname = target_dir / f"{slug}_{counter:02d}.wav"
                    metadata = {
                        "title": p_eff_list[i - 1],
                        "artist": "Stable Audio Insight",
                        "software": f"Stable Audio Open 1.0 / {get_model_id()}",
                        "creation_date": time.strftime("%Y-%m-%d"),
                        "comment": f"seed={seeds[i-1]}; batch_index={i}; mode=all; duration={seconds:.1f}s; steps={steps}; cfg={cfg}; sample_rate={SAMPLE_RATE}Hz",
                    }
                    write_wav_with_metadata(fname, audio, SAMPLE_RATE, metadata)
                    results.append(f"{i}/{len(lines)}: {fname.name}")
                    if i - 1 < MAX_BATCH_PREVIEW:
                        previews[i - 1] = gr.update(
                            value=_mini_audio_html(str(fname), f"#{i}: {p_eff_list[i-1][:60]}"),
                            visible=True,
                        )
                except Exception as e:
                    log.exception(f"batch-all post item {i} failed")
                    results.append(f"{i}/{len(lines)}: ERROR - {e}")
            del res
            _free_cuda()
        except torch.cuda.OutOfMemoryError as e:
            _free_cuda()
            log.exception("batch-all CUDA OOM")
            results.append(f"ERROR: CUDA OOM in all-at-once mode — try fewer prompts, shorter duration, or switch to one-by-one. ({e})")
        except Exception as e:
            _free_cuda()
            log.exception("batch-all failed")
            results.append(f"ERROR: {e}")

        final_status = "\n".join(results) if results else "Batch finished (no items processed)."
        yield (final_status, *previews)
        return

    yield (f"Starting batch: {len(lines)} prompt(s)…", *previews)

    for i, p in enumerate(lines, start=1):
        try:
            p_eff = _translator.translate(p) if needs_translation(p) else p
            seed = int(torch.randint(0, 2**31 - 1, (1,)).item())
            generator = torch.Generator(device=str(pipe.device).split(":")[0]).manual_seed(seed)
            log.info(f"batch {i}/{len(lines)} prompt='{p_eff[:60]}' seed={seed}")
            _free_cuda()
            def _do_batch_pipe(s):
                return pipe(
                    prompt=p_eff,
                    negative_prompt=n_eff or None,
                    num_inference_steps=s,
                    audio_end_in_s=seconds,
                    guidance_scale=cfg,
                    generator=generator,
                )
            try:
                res = _do_batch_pipe(steps)
            except IndexError as ie:
                if "out of bounds" in str(ie).lower():
                    log.warning(f"batch {i}: scheduler IndexError; retrying with steps={steps+2}")
                    _free_cuda()
                    generator = torch.Generator(device=str(pipe.device).split(":")[0]).manual_seed(seed)
                    res = _do_batch_pipe(steps + 2)
                else:
                    raise
            audio = post_audio(res.audios[0])
            slug = slugify_prompt(p_eff)
            counter = next_counter(target_dir, slug)
            fname = target_dir / f"{slug}_{counter:02d}.wav"
            metadata = {
                "title": p_eff,
                "artist": "Stable Audio Insight",
                "software": f"Stable Audio Open 1.0 / {get_model_id()}",
                "creation_date": time.strftime("%Y-%m-%d"),
                "comment": f"seed={seed}; batch_index={i}; duration={seconds:.1f}s; steps={steps}; cfg={cfg}; sample_rate={SAMPLE_RATE}Hz",
            }
            write_wav_with_metadata(fname, audio, SAMPLE_RATE, metadata)
            results.append(f"{i}/{len(lines)}: {fname.name}")
            log.info(f"batch ok {results[-1]}")
            del res
            _free_cuda()
            slot = i - 1
            if slot < MAX_BATCH_PREVIEW:
                previews[slot] = gr.update(
                    value=_mini_audio_html(str(fname), f"#{i}: {p_eff[:60]}"),
                    visible=True,
                )
        except Exception as e:
            log.exception(f"batch item {i} failed")
            results.append(f"{i}/{len(lines)}: ERROR - {e}")
        yield ("\n".join(results), *previews)

    final_status = "\n".join(results) if results else "Batch finished (no items processed)."
    yield (final_status, *previews)


def clear_intermediate() -> str:
    if not INTERMEDIATE_DIR.exists():
        return "outputs/intermediate is already empty (folder does not exist)."
    files = [f for f in INTERMEDIATE_DIR.iterdir() if f.is_file() and f.suffix.lower() == ".wav"]
    if not files:
        return "outputs/intermediate is already empty."
    deleted = 0
    failed: list[str] = []
    for f in files:
        try:
            f.unlink()
            deleted += 1
        except Exception as e:
            failed.append(f"{f.name}: {e}")
    msg = f"Cleared {deleted} file(s) from outputs/intermediate."
    if failed:
        msg += f" {len(failed)} failed: {'; '.join(failed[:3])}"
    log.info(msg)
    return msg


def export_zip():
    if not SAVED_DIR.exists():
        return None, "No outputs/Saved directory yet."
    files = [f for f in SAVED_DIR.iterdir() if f.is_file() and f.suffix.lower() == ".wav"]
    if not files:
        return None, "No saved audio files yet."
    zip_path = TMP_DIR / f"stable-audio-saved-{time.strftime('%Y%m%d-%H%M%S')}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.write(f, f.name)
    return str(zip_path), f"Zipped {len(files)} files: {zip_path.name}"


def save_selected(*paths: str) -> str:
    SAVED_DIR.mkdir(parents=True, exist_ok=True)
    saved_names: list[str] = []
    for p in paths:
        if not p:
            continue
        src = Path(p)
        if not src.exists():
            continue
        m = re.match(r"^(.+)_\d+\.wav$", src.name, re.IGNORECASE)
        slug = m.group(1) if m else src.stem
        counter = next_counter(SAVED_DIR, slug)
        dst = SAVED_DIR / f"{slug}_{counter:02d}.wav"
        shutil.copy2(src, dst)
        saved_names.append(dst.name)
    if not saved_names:
        return "Nothing to save — generate audio first."
    if len(saved_names) == 1:
        return f"Saved: outputs/Saved/{saved_names[0]}"
    return f"Saved {len(saved_names)} files: {', '.join(saved_names)}"

gpu_name = torch.cuda.get_device_name(0) if device == "cuda" else "CPU"
i18n = gr.I18n(**TRANSLATIONS)

CUSTOM_CSS = """
/* Hide built-in tab navigation: category selection is driven by the
   Dropdown above the Tabs. Keeps the reliable Tabs content rendering
   without the horizontal-scroll / 3-dots overflow problem. */
.presets-tabs > .tab-nav,
.presets-tabs > div:first-child {
    display: none !important;
}
/* Tab content panel: fixed height + scroll, so UI does not jump
   when switching between categories with different button counts. */
.presets-tabs > .tabitem,
.presets-tabs > div[role="tabpanel"] {
    height: 240px;
    overflow-y: auto;
    padding-right: 4px;
}
/* Compact dropdown for category selection */
.cat-dropdown {
    margin-bottom: 4px;
}
/* Framed intro card at the top of the page */
.intro-card {
    border: 1px solid var(--border-color-primary, #444);
    border-radius: 10px;
    padding: 14px 18px 6px 18px;
    margin-bottom: 6px;
    background: var(--background-fill-secondary, rgba(127,127,127,0.05));
}
.intro-card h1, .intro-card h2 { margin-top: 0; }
.status-bar {
    font-size: 13px;
    opacity: 0.85;
    padding: 4px 4px 10px 4px;
}
/* Bottom-of-page persistent log */
.bottom-log {
    margin-top: 14px;
    border-top: 1px solid var(--border-color-primary, #444);
    padding-top: 10px;
}
.bottom-log textarea {
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: 12px;
}
/* Mini audio for history and batch previews — native HTML5 <audio>,
   thin standard browser controls with play/seek/volume. */
.mini-audio {
    padding: 0 !important;
    margin: 0 !important;
    min-height: 0 !important;
    border: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
}
.mini-audio > div { padding: 0 !important; margin: 0 !important; }
.mini-track {
    display: flex;
    flex-direction: column;
    gap: 0 !important;
    padding: 3px 4px !important;
    border-bottom: 1px solid rgba(127,127,127,0.25);
}
.mini-label { font-size: 11px; opacity: 0.75; line-height: 1.2; }
.mini-track audio { display: block; height: 28px !important; }
/* Eliminate the gap that Gradio puts between successive components */
.mini-audio + .mini-audio { margin-top: 0 !important; }
/* Scrollable container for the global Recent generations accordion */
.history-scroll {
    max-height: 320px;
    overflow-y: auto;
    padding-right: 4px;
}
.history-accordion { margin-top: 8px; }
"""

with gr.Blocks(title="Stable Audio Insight") as demo:
    with gr.Column(elem_classes=["intro-card"]):
        gr.Markdown("# 🎵 Stable Audio Insight")
        gr.Markdown(
            f"GPU: **{gpu_name}** · Model: `{MODEL_ID}` · "
            f"Translator: `{get_model_id()}` ({get_kind()}) · "
            f"Max duration ~ {MAX_DURATION:.0f} sec",
            elem_classes=["status-bar"],
        )

    preset_clicks = []
    _cat_keys_list = list(PRESETS.keys())
    _default_cat = _cat_keys_list[0]
    # English labels for dropdown (gr.Dropdown choices don't expand i18n).
    _cat_en = {k: TRANSLATIONS["en"][k] for k in _cat_keys_list}
    _label_to_key = {_cat_en[k]: k for k in _cat_keys_list}

    with gr.Tabs():
        with gr.Tab(i18n("main_tab")):
            with gr.Row():
                with gr.Column(scale=2):
                    prompt = gr.Textbox(
                        label=i18n("prompt_label"),
                        lines=3,
                        placeholder="128 BPM tech house drum loop with crisp hi-hats",
                    )
                    translation_out = gr.Textbox(
                        label=i18n("translation_label"),
                        lines=2,
                        interactive=False,
                        placeholder=i18n("translation_placeholder"),
                    )
                    negative = gr.Textbox(
                        label=i18n("negative_label"),
                        lines=3,
                        value="low quality, average quality, noisy, muffled, distorted, amateur, lo-fi recording",
                    )
                    with gr.Accordion(i18n("presets_title"), open=False):
                        cat_dropdown = gr.Dropdown(
                            choices=[_cat_en[k] for k in _cat_keys_list],
                            value=_cat_en[_default_cat],
                            label="Category",
                            show_label=True,
                            interactive=True,
                            elem_classes=["cat-dropdown"],
                        )
                        with gr.Tabs(selected=_default_cat, elem_classes=["presets-tabs"]) as cat_tabs:
                            for cat_key, items in PRESETS.items():
                                with gr.Tab(i18n(cat_key), id=cat_key):
                                    for i in range(0, len(items), 4):
                                        with gr.Row():
                                            for label_key, full_prompt in items[i:i+4]:
                                                b = gr.Button(i18n(label_key), size="sm")
                                                preset_clicks.append((b, full_prompt))

                        cat_dropdown.change(
                            lambda label: gr.Tabs(selected=_label_to_key.get(label, _default_cat)),
                            inputs=cat_dropdown,
                            outputs=cat_tabs,
                            queue=False,
                            show_progress="hidden",
                        )
                    with gr.Row():
                        seconds = gr.Slider(1, MAX_DURATION, value=10, step=0.5, label=i18n("duration_label"))
                        steps = gr.Slider(10, 250, value=100, step=1, label=i18n("steps_label"))
                    with gr.Row():
                        cfg = gr.Slider(1.0, 15.0, value=7.0, step=0.5, label=i18n("cfg_label"))
                        with gr.Column(scale=2):
                            seed = gr.Number(value=-1, label=i18n("seed_label"), precision=0)
                            random_seed_btn = gr.Button(i18n("random_seed_btn"), size="sm", variant="secondary")
                    with gr.Row():
                        btn = gr.Button(i18n("generate_btn"), variant="primary", size="lg", scale=3)
                        reroll_btn = gr.Button(i18n("reroll_btn"), variant="secondary", size="lg", scale=1)
                        cancel_btn = gr.Button(i18n("cancel_btn"), variant="stop", size="lg", scale=1)

                with gr.Column(scale=1):
                    variations = gr.Slider(1, MAX_VARIATIONS, value=1, step=1, label=i18n("variations_label"))
                    audio_outs = []
                    for i in range(MAX_VARIATIONS):
                        a = gr.Audio(
                            label=(i18n("result_label") if i == 0 else f"Variation {i+1}"),
                            type="filepath",
                            autoplay=False,
                            interactive=False,
                            visible=(i == 0),
                        )
                        audio_outs.append(a)
                    save_btn = gr.Button(i18n("save_btn"), size="sm")
                    with gr.Accordion(i18n("history_title"), open=False, elem_classes=["history-accordion"]):
                        with gr.Column(elem_classes=["history-scroll"]):
                            main_history_audios = []
                            for i in range(HISTORY_SIZE):
                                a = gr.HTML(value="", visible=False, elem_classes=["mini-audio"])
                                main_history_audios.append(a)

        with gr.Tab(i18n("batch_tab")):
            with gr.Row():
                with gr.Column(scale=2):
                    batch_prompts_box = gr.Textbox(
                        label=i18n("batch_prompts_label"),
                        lines=8,
                        max_lines=30,
                        placeholder="footsteps on wood\nrain on roof\n128 BPM tech house\nкрик ворона в лесу",
                        interactive=True,
                    )
                    batch_translation_out = gr.Textbox(
                        label=i18n("batch_translation_label"),
                        lines=4,
                        max_lines=30,
                        interactive=False,
                        placeholder=i18n("batch_translation_placeholder"),
                    )
                    batch_negative = gr.Textbox(
                        label=i18n("negative_label"),
                        lines=2,
                        value="low quality, average quality, noisy, muffled, distorted, amateur, lo-fi recording",
                    )
                    with gr.Row():
                        batch_seconds = gr.Slider(1, MAX_DURATION, value=10, step=0.5, label=i18n("duration_label"))
                        batch_steps = gr.Slider(10, 250, value=100, step=1, label=i18n("steps_label"))
                        batch_cfg = gr.Slider(1.0, 15.0, value=7.0, step=0.5, label=i18n("cfg_label"))
                    batch_all_at_once = gr.Checkbox(
                        value=False,
                        label=i18n("batch_mode_all"),
                        interactive=True,
                    )
                    with gr.Row():
                        batch_btn = gr.Button(i18n("batch_run_btn"), variant="primary", size="lg", scale=3)
                        batch_cancel_btn = gr.Button(i18n("cancel_btn"), variant="stop", size="lg", scale=1)

                with gr.Column(scale=1):
                    batch_status = gr.Textbox(label=i18n("batch_status_label"), lines=4, interactive=False)
                    batch_previews = []
                    for i in range(MAX_BATCH_PREVIEW):
                        a = gr.HTML(value="", visible=False, elem_classes=["mini-audio"])
                        batch_previews.append(a)
                    zip_btn = gr.Button(i18n("zip_export_btn_v2"), variant="secondary", size="sm")
                    zip_file = gr.File(label="ZIP", visible=False, interactive=False)
                    with gr.Accordion(i18n("history_title"), open=False, elem_classes=["history-accordion"]):
                        with gr.Column(elem_classes=["history-scroll"]):
                            batch_history_audios = []
                            for i in range(HISTORY_SIZE):
                                a = gr.HTML(value="", visible=False, elem_classes=["mini-audio"])
                                batch_history_audios.append(a)

        with gr.Tab(i18n("settings_tab")):
            gr.Markdown(i18n("settings_intro_md"))
            with gr.Row():
                device_radio = gr.Radio(
                    choices=["GPU", "CPU"],
                    value=("GPU" if device == "cuda" else "CPU"),
                    label=i18n("device_label"),
                    interactive=True,
                )
                scheduler_dd = gr.Dropdown(
                    choices=SCHEDULERS, value="Default", label=i18n("scheduler_label"), interactive=True,
                )
            save_all = gr.Checkbox(label=i18n("save_all_label"), value=False)
            clear_intermediate_btn = gr.Button(i18n("clear_intermediate_btn"), variant="secondary", size="sm")
            gr.Markdown(i18n("scheduler_help_md"))
            gr.Markdown("---")
            gr.Markdown(i18n("info_md"))

    history_state = gr.State([])

    gen_info_state = gr.State("")
    with gr.Column(elem_classes=["bottom-log"]):
        info_out = gr.Textbox(
            label=i18n("log_label"),
            lines=6,
            max_lines=20,
            interactive=False,
        )

    for b, p in preset_clicks:
        b.click(lambda x=p: x, outputs=prompt)

    prompt.change(
        live_translate,
        inputs=[prompt],
        outputs=[translation_out],
        show_progress="hidden",
    )

    def _build_history_updates(new_hist: list) -> list:
        out = []
        for i in range(HISTORY_SIZE):
            if i < len(new_hist):
                p = new_hist[i]
                label = Path(p).name
                out.append(gr.update(value=_mini_audio_html(p, f"#{i+1} · {label}"), visible=True))
            else:
                out.append(gr.update(value="", visible=False))
        return out

    def _push_to_history(*args):
        *new_paths, current_history = args
        fresh = [p for p in new_paths if p]
        if not fresh:
            no_change = [gr.update() for _ in range(HISTORY_SIZE * 2)]
            return [current_history or []] + no_change
        new_hist = fresh + [p for p in (current_history or []) if p not in fresh]
        new_hist = new_hist[:HISTORY_SIZE]
        u1 = _build_history_updates(new_hist)
        u2 = _build_history_updates(new_hist)
        return [new_hist] + u1 + u2

    _gen_clear = btn.click(
        clear_audio_slots,
        inputs=[variations],
        outputs=audio_outs,
        queue=False,
        show_progress="hidden",
    )
    gen_event = _gen_clear.then(
        generate,
        inputs=[prompt, negative, seconds, steps, cfg, seed, save_all, variations],
        outputs=[*audio_outs, gen_info_state],
    )
    gen_event.then(
        _append_log,
        inputs=[gen_info_state, info_out],
        outputs=info_out,
        queue=False,
        show_progress="hidden",
    )
    gen_event.then(
        _push_to_history,
        inputs=[*audio_outs, history_state],
        outputs=[history_state, *main_history_audios, *batch_history_audios],
        queue=False,
        show_progress="hidden",
    )

    random_seed_btn.click(
        lambda: int(torch.randint(0, 2**31 - 1, (1,)).item()),
        outputs=seed,
        queue=False,
        show_progress="hidden",
    )

    def _reroll(p, n, s, st, c, _seed_unused, sa, v, progress=gr.Progress(track_tqdm=True)):
        return generate(p, n, s, st, c, -1, sa, v, progress)

    _reroll_clear = reroll_btn.click(
        clear_audio_slots,
        inputs=[variations],
        outputs=audio_outs,
        queue=False,
        show_progress="hidden",
    )
    reroll_event = _reroll_clear.then(
        _reroll,
        inputs=[prompt, negative, seconds, steps, cfg, seed, save_all, variations],
        outputs=[*audio_outs, gen_info_state],
    )
    reroll_event.then(
        _append_log,
        inputs=[gen_info_state, info_out],
        outputs=info_out,
        queue=False,
        show_progress="hidden",
    )
    reroll_event.then(
        _push_to_history,
        inputs=[*audio_outs, history_state],
        outputs=[history_state, *main_history_audios, *batch_history_audios],
        queue=False,
        show_progress="hidden",
    )

    save_event = save_btn.click(
        save_selected,
        inputs=audio_outs,
        outputs=gen_info_state,
        queue=False,
        show_progress="hidden",
    )
    save_event.then(
        _append_log,
        inputs=[gen_info_state, info_out],
        outputs=info_out,
        queue=False,
        show_progress="hidden",
    )

    variations.release(
        lambda n: [gr.update(visible=(i < int(n))) for i in range(MAX_VARIATIONS)],
        inputs=variations,
        outputs=audio_outs,
        queue=False,
        show_progress="hidden",
    )

    sched_event = scheduler_dd.change(
        set_scheduler,
        inputs=scheduler_dd,
        outputs=gen_info_state,
        queue=False,
        show_progress="hidden",
    )
    sched_event.then(
        _append_log,
        inputs=[gen_info_state, info_out],
        outputs=info_out,
        queue=False,
        show_progress="hidden",
    )

    device_event = device_radio.change(
        set_device,
        inputs=device_radio,
        outputs=gen_info_state,
        queue=False,
    )
    device_event.then(
        _append_log,
        inputs=[gen_info_state, info_out],
        outputs=info_out,
        queue=False,
        show_progress="hidden",
    )

    batch_prompts_box.change(
        live_translate_batch,
        inputs=[batch_prompts_box],
        outputs=[batch_translation_out],
        show_progress="hidden",
    )

    def _clear_batch_previews():
        return [gr.update(value="", visible=False) for _ in range(MAX_BATCH_PREVIEW)]

    _batch_clear = batch_btn.click(
        _clear_batch_previews,
        outputs=batch_previews,
        queue=False,
        show_progress="hidden",
    )
    batch_event = _batch_clear.then(
        generate_batch,
        inputs=[batch_prompts_box, batch_negative, batch_seconds, batch_steps, batch_cfg, batch_all_at_once, save_all],
        outputs=[batch_status, *batch_previews],
    )

    def _push_batch_to_history(*args):
        *preview_html, current_history = args
        import re as _re
        from urllib.parse import unquote
        new_paths: list[str] = []
        for h in preview_html:
            if not h:
                continue
            m = _re.search(r'/gradio_api/file=([^"\s]+)', str(h))
            if m:
                new_paths.append(unquote(m.group(1)))
        if not new_paths:
            no_change = [gr.update() for _ in range(HISTORY_SIZE * 2)]
            return [current_history or []] + no_change
        recent_first = list(reversed(new_paths))
        new_hist = recent_first + [p for p in (current_history or []) if p not in recent_first]
        new_hist = new_hist[:HISTORY_SIZE]
        u1 = _build_history_updates(new_hist)
        u2 = _build_history_updates(new_hist)
        return [new_hist] + u1 + u2

    batch_event.then(
        _push_batch_to_history,
        inputs=[*batch_previews, history_state],
        outputs=[history_state, *main_history_audios, *batch_history_audios],
        queue=False,
        show_progress="hidden",
    )

    batch_event.then(
        lambda s: f"Batch finished:\n{s}" if s else "Batch finished (empty).",
        inputs=batch_status,
        outputs=gen_info_state,
        queue=False,
        show_progress="hidden",
    ).then(
        _append_log,
        inputs=[gen_info_state, info_out],
        outputs=info_out,
        queue=False,
        show_progress="hidden",
    )

    def _cancel_msg():
        log.info("user cancelled generation")
        _free_cuda()
        return "Cancelled."

    def _batch_cancel_msg():
        log.info("user cancelled generation (from batch tab)")
        _free_cuda()
        return "Cancelled."

    cancel_event = cancel_btn.click(
        _cancel_msg,
        outputs=gen_info_state,
        cancels=[gen_event, reroll_event, batch_event],
        queue=False,
        show_progress="hidden",
    )
    cancel_event.then(
        _append_log,
        inputs=[gen_info_state, info_out],
        outputs=info_out,
        queue=False,
        show_progress="hidden",
    )

    batch_cancel_event = batch_cancel_btn.click(
        _batch_cancel_msg,
        outputs=batch_status,
        cancels=[gen_event, reroll_event, batch_event],
        queue=False,
        show_progress="hidden",
    )
    batch_cancel_event.then(
        lambda: "Batch cancelled.",
        outputs=gen_info_state,
        queue=False,
        show_progress="hidden",
    ).then(
        _append_log,
        inputs=[gen_info_state, info_out],
        outputs=info_out,
        queue=False,
        show_progress="hidden",
    )

    clear_inter_event = clear_intermediate_btn.click(
        clear_intermediate,
        outputs=gen_info_state,
        queue=False,
        show_progress="hidden",
    )
    clear_inter_event.then(
        _append_log,
        inputs=[gen_info_state, info_out],
        outputs=info_out,
        queue=False,
        show_progress="hidden",
    )

    def _do_zip(*preview_values):
        import re as _re
        from urllib.parse import unquote
        paths: list[str] = []
        for h in preview_values:
            if not h:
                continue
            m = _re.search(r'/gradio_api/file=([^"\s]+)', str(h))
            if m:
                paths.append(unquote(m.group(1)))
        if not paths:
            return gr.update(visible=False), "Nothing to zip — run a batch first."
        zip_path = TMP_DIR / f"stable-audio-batch-{time.strftime('%Y%m%d-%H%M%S')}.zip"
        zipped = 0
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for p in paths:
                pp = Path(p)
                if pp.exists():
                    zf.write(pp, pp.name)
                    zipped += 1
        if zipped == 0:
            return gr.update(visible=False), "Nothing to zip — files are missing."
        return gr.update(value=str(zip_path), visible=True), f"Zipped {zipped} files: {zip_path.name}"

    zip_btn.click(
        _do_zip,
        inputs=batch_previews,
        outputs=[zip_file, batch_status],
        queue=False,
    )

    gr.Markdown(
        "<div style='text-align:center;font-size:13px;opacity:0.8;"
        "margin-top:18px;padding-top:10px;border-top:1px solid var(--border-color-primary);'>"
        "Stable Audio Open 1.0 © Stability AI · Stable Audio Insight by "
        "<a href='https://www.io-oscar.com/' target='_blank' "
        "style='color:inherit;text-decoration:underline;'>Oscar Lumiere</a>"
        "</div>"
    )


if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "7860"))
    share = os.environ.get("SHARE", "0") == "1"
    demo.queue().launch(
        server_name=host,
        server_port=port,
        share=share,
        inbrowser=True,
        i18n=i18n,
        css=CUSTOM_CSS,
        allowed_paths=[str(TMP_DIR), str(OUTPUTS_ROOT)],
    )
