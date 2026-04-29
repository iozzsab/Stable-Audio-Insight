import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.environ.setdefault("HF_HOME", str(ROOT / "hf-cache"))

from huggingface_hub import snapshot_download, get_token
from huggingface_hub.utils import HfHubHTTPError

from translator import get_kind, get_model_id

MODEL_ID = "stabilityai/stable-audio-open-1.0"


def download_audio_model() -> int:
    token = (
        os.environ.get("HF_TOKEN")
        or os.environ.get("HUGGING_FACE_HUB_TOKEN")
        or get_token()
    )
    if not token:
        print("ERROR: HuggingFace token not found.")
        print()
        print("Run `install.bat` (or `login.bat`) once, or set HF_TOKEN before launching:")
        print("  set HF_TOKEN=hf_xxxxx && download.bat")
        print()
        print("Get a token (read access): https://huggingface.co/settings/tokens")
        print(f"Accept license here:        https://huggingface.co/{MODEL_ID}")
        return 1

    print(f"Cache dir : {os.environ['HF_HOME']}")
    print(f"Audio model : {MODEL_ID}")
    print("Downloading audio model (~5 GB, can take a while)...")
    try:
        path = snapshot_download(
            repo_id=MODEL_ID,
            token=token,
            allow_patterns=[
                "*.json",
                "*.txt",
                "*.md",
                "*.safetensors",
                "*.model",
                "tokenizer*",
                "spiece.model",
            ],
        )
    except HfHubHTTPError as e:
        msg = str(e)
        if "401" in msg or "403" in msg or "gated" in msg.lower():
            print("ERROR: access denied. Make sure you accepted the license:")
            print(f"  https://huggingface.co/{MODEL_ID}")
        else:
            print(f"ERROR: {e}")
        return 2

    print(f"Audio model snapshot at: {path}")
    return 0


def download_translator() -> int:
    kind = get_kind()
    model_id = get_model_id(kind)
    print()
    print(f"Translator : {model_id} (kind={kind})")
    size_hint = "~300 MB" if kind == "light" else "~2.4 GB"
    print(f"Downloading translator ({size_hint})...")
    try:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        AutoTokenizer.from_pretrained(model_id)
        AutoModelForSeq2SeqLM.from_pretrained(model_id)
    except Exception as e:
        print(f"ERROR: failed to download translator: {e}")
        return 3
    print("Translator downloaded.")
    return 0


def main() -> int:
    rc = download_audio_model()
    if rc != 0:
        return rc
    return download_translator()


if __name__ == "__main__":
    sys.exit(main())
