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


def generate(prompt: str, negative: str, seconds: float, steps: int, cfg: float, seed: int, save_all: bool, variations: int, progress=gr.Progress(track_tqdm=True)):
    if not prompt or not prompt.strip():
        raise gr.Error("Enter a prompt")
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

        result = pipe(
            prompt=prompt,
            negative_prompt=negative or None,
            num_inference_steps=steps,
            audio_end_in_s=seconds,
            guidance_scale=cfg,
            generator=generator,
            num_waveforms_per_prompt=variations,
        )

        slug = slugify_prompt(prompt)
        paths: list[str | None] = [None] * MAX_VARIATIONS
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
            paths[i] = str(fname)
            written_names.append(fname.name)
            if save_all:
                INTERMEDIATE_DIR.mkdir(parents=True, exist_ok=True)
                ic = next_counter(INTERMEDIATE_DIR, slug)
                shutil.copy2(fname, INTERMEDIATE_DIR / f"{slug}_{ic:02d}.wav")

        elapsed = time.time() - t0
        info = f"seed={seed} | {seconds:.1f}s @ {SAMPLE_RATE} Hz | {steps} steps | {variations} var(s) | {elapsed:.1f}s gen"
        info += "\n" + ", ".join(written_names)
        if save_all:
            info += "\n-> copies in outputs/intermediate/"
        log.info(f"gen done: {info}")
        return paths[0], paths[1], paths[2], paths[3], info
    except torch.cuda.OutOfMemoryError as e:
        log.exception("CUDA out of memory")
        raise gr.Error(f"CUDA out of memory — try fewer variations or shorter duration. ({e})")
    except Exception as e:
        log.exception("generate() failed")
        raise gr.Error(f"Generation failed: {e}. See log file for full traceback.")


def generate_batch(batch_prompts: str, negative: str, seconds: float, steps: int, cfg: float, progress=gr.Progress(track_tqdm=True)):
    if not batch_prompts or not batch_prompts.strip():
        return "Empty batch — paste prompts (one per line)."
    lines = [s.strip() for s in batch_prompts.splitlines() if s.strip()]
    if not lines:
        return "Empty batch — paste prompts (one per line)."
    SAVED_DIR.mkdir(parents=True, exist_ok=True)
    n_eff = _translator.translate(negative) if needs_translation(negative) else (negative or "")
    seconds = float(min(max(seconds, 1.0), MAX_DURATION))
    steps = int(steps)
    cfg = float(cfg)
    results: list[str] = []
    for i, p in enumerate(lines, start=1):
        try:
            p_eff = _translator.translate(p) if needs_translation(p) else p
            seed = int(torch.randint(0, 2**31 - 1, (1,)).item())
            generator = torch.Generator(device=str(pipe.device).split(":")[0]).manual_seed(seed)
            log.info(f"batch {i}/{len(lines)} prompt='{p_eff[:60]}' seed={seed}")
            res = pipe(
                prompt=p_eff,
                negative_prompt=n_eff or None,
                num_inference_steps=steps,
                audio_end_in_s=seconds,
                guidance_scale=cfg,
                generator=generator,
            )
            audio = post_audio(res.audios[0])
            slug = slugify_prompt(p_eff)
            counter = next_counter(SAVED_DIR, slug)
            fname = SAVED_DIR / f"{slug}_{counter:02d}.wav"
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
        except Exception as e:
            log.exception(f"batch item {i} failed")
            results.append(f"{i}/{len(lines)}: ERROR - {e}")
    return "\n".join(results)


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
"""

with gr.Blocks(title="Stable Audio Insight") as demo:
    gr.Markdown(i18n("info_md"))
    gr.Markdown(
        f"GPU: **{gpu_name}** · Model: `{MODEL_ID}` · "
        f"Translator: `{get_model_id()}` ({get_kind()}) · "
        f"Max duration ~ {MAX_DURATION:.0f} sec"
    )

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
            preset_clicks = []
            _cat_keys_list = list(PRESETS.keys())
            _default_cat = _cat_keys_list[0]
            # English labels for dropdown (gr.Dropdown choices don't expand i18n).
            _cat_en = {k: TRANSLATIONS["en"][k] for k in _cat_keys_list}
            _label_to_key = {_cat_en[k]: k for k in _cat_keys_list}
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
                variations = gr.Slider(1, MAX_VARIATIONS, value=1, step=1, label=i18n("variations_label"))
                scheduler_dd = gr.Dropdown(
                    choices=SCHEDULERS, value="Default", label=i18n("scheduler_label"), interactive=True,
                )
            with gr.Row():
                device_radio = gr.Radio(
                    choices=["GPU", "CPU"],
                    value=("GPU" if device == "cuda" else "CPU"),
                    label="Device (GPU = fast / CPU = compatible, slow)",
                    interactive=True,
                )
            with gr.Row():
                btn = gr.Button(i18n("generate_btn"), variant="primary", size="lg", scale=3)
                reroll_btn = gr.Button(i18n("reroll_btn"), variant="secondary", size="lg", scale=1)

        with gr.Column(scale=1):
            save_all = gr.Checkbox(label=i18n("save_all_label"), value=False)
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
            info_out = gr.Textbox(label=i18n("log_label"), lines=4, interactive=False)
            history_state = gr.State([])
            with gr.Accordion(i18n("history_title"), open=False):
                history_audios = []
                for i in range(HISTORY_SIZE):
                    a = gr.Audio(
                        label=f"#{i+1}",
                        type="filepath",
                        autoplay=False,
                        interactive=False,
                        visible=False,
                    )
                    history_audios.append(a)

            with gr.Accordion(i18n("batch_title"), open=False):
                batch_prompts_box = gr.Textbox(
                    label=i18n("batch_prompts_label"),
                    lines=5,
                    placeholder="footsteps on wood\nrain on roof\n128 BPM tech house",
                )
                with gr.Row():
                    batch_btn = gr.Button(i18n("batch_run_btn"), variant="primary", size="sm")
                    zip_btn = gr.Button(i18n("zip_export_btn"), variant="secondary", size="sm")
                batch_status = gr.Textbox(label=i18n("batch_status_label"), lines=4, interactive=False)
                zip_file = gr.File(label="ZIP", visible=False, interactive=False)

    for b, p in preset_clicks:
        b.click(lambda x=p: x, outputs=prompt)

    prompt.change(
        live_translate,
        inputs=[prompt],
        outputs=[translation_out],
        show_progress="hidden",
    )

    def _push_to_history(new_path, current_history):
        if not new_path:
            return [current_history or []] + [gr.update() for _ in range(HISTORY_SIZE)]
        new_hist = [new_path] + [p for p in (current_history or []) if p != new_path]
        new_hist = new_hist[:HISTORY_SIZE]
        updates = []
        for i in range(HISTORY_SIZE):
            if i < len(new_hist):
                updates.append(gr.update(value=new_hist[i], visible=True))
            else:
                updates.append(gr.update(value=None, visible=False))
        return [new_hist] + updates

    btn.click(
        generate,
        inputs=[prompt, negative, seconds, steps, cfg, seed, save_all, variations],
        outputs=[*audio_outs, info_out],
    ).then(
        _push_to_history,
        inputs=[audio_outs[0], history_state],
        outputs=[history_state, *history_audios],
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

    reroll_btn.click(
        _reroll,
        inputs=[prompt, negative, seconds, steps, cfg, seed, save_all, variations],
        outputs=[*audio_outs, info_out],
    ).then(
        _push_to_history,
        inputs=[audio_outs[0], history_state],
        outputs=[history_state, *history_audios],
        queue=False,
        show_progress="hidden",
    )

    save_btn.click(
        save_selected,
        inputs=audio_outs,
        outputs=[info_out],
    )

    variations.change(
        lambda n: [gr.update(visible=(i < int(n))) for i in range(MAX_VARIATIONS)],
        inputs=variations,
        outputs=audio_outs,
        queue=False,
        show_progress="hidden",
    )

    scheduler_dd.change(
        set_scheduler,
        inputs=scheduler_dd,
        outputs=info_out,
        queue=False,
        show_progress="hidden",
    )

    device_radio.change(
        set_device,
        inputs=device_radio,
        outputs=info_out,
        queue=False,
    )

    batch_btn.click(
        generate_batch,
        inputs=[batch_prompts_box, negative, seconds, steps, cfg],
        outputs=batch_status,
    )

    def _do_zip():
        path, msg = export_zip()
        if path is None:
            return gr.update(visible=False), msg
        return gr.update(value=path, visible=True), msg

    zip_btn.click(
        _do_zip,
        outputs=[zip_file, batch_status],
        queue=False,
    )

    gr.Markdown(
        "<div style='text-align:center;font-size:13px;opacity:0.8;"
        "margin-top:18px;padding-top:10px;border-top:1px solid var(--border-color-primary);'>"
        "Stable Audio Open 1.0 © Stability AI · Stable Audio Insight by Oscar Lumiere"
        "</div>"
    )


if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "7860"))
    share = os.environ.get("SHARE", "0") == "1"
    demo.queue().launch(server_name=host, server_port=port, share=share, inbrowser=True, i18n=i18n, css=CUSTOM_CSS)
