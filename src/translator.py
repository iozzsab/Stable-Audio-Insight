import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = ROOT / "hf-cache" / "translator.cfg"
_LEGACY_CONFIG = ROOT / "translator.cfg"

TRANSLATOR_MODELS = {
    "light": "Helsinki-NLP/opus-mt-mul-en",
    "heavy": "facebook/nllb-200-distilled-600M",
}

SCRIPT_RANGES = [
    ("ru", r"[Ѐ-ӿ]"),
    ("zh", r"[一-鿿]"),
    ("ja", r"[぀-ゟ゠-ヿ]"),
    ("ko", r"[가-힯]"),
    ("ar", r"[؀-ۿ]"),
    ("he", r"[֐-׿]"),
    ("el", r"[Ͱ-Ͽ]"),
    ("th", r"[฀-๿]"),
    ("hi", r"[ऀ-ॿ]"),
]
NON_LATIN_RE = re.compile("|".join(p for _, p in SCRIPT_RANGES))

NLLB_LANG = {
    "ru": "rus_Cyrl",
    "zh": "zho_Hans",
    "ja": "jpn_Jpan",
    "ko": "kor_Hang",
    "ar": "arb_Arab",
    "he": "heb_Hebr",
    "el": "ell_Grek",
    "th": "tha_Thai",
    "hi": "hin_Deva",
}


def get_kind() -> str:
    for path in (CONFIG_FILE, _LEGACY_CONFIG):
        if path.exists():
            v = path.read_text(encoding="utf-8").strip().lower()
            if v in TRANSLATOR_MODELS:
                return v
    return "light"


def get_model_id(kind: str | None = None) -> str:
    return TRANSLATOR_MODELS[kind or get_kind()]


def needs_translation(text: str) -> bool:
    return bool(text and NON_LATIN_RE.search(text))


def _detect_iso(text: str) -> str:
    for iso, pat in SCRIPT_RANGES:
        if re.search(pat, text):
            return iso
    return "en"


class Translator:
    def __init__(self):
        self.kind = get_kind()
        self.model_id = TRANSLATOR_MODELS[self.kind]
        self._tokenizer = None
        self._model = None

    def _ensure_loaded(self):
        if self._model is not None:
            return
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        print(f"[init] loading translator {self.model_id} (kind={self.kind})...")
        self._tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self._model = AutoModelForSeq2SeqLM.from_pretrained(self.model_id)
        print("[init] translator ready.")

    def translate(self, text: str) -> str:
        if not text:
            return ""
        self._ensure_loaded()
        segments = [s.strip() for s in re.split(r"[,;]\s*", text.strip()) if s.strip()]
        is_tag_style = len(segments) >= 2 and all(len(s.split()) <= 5 for s in segments)
        if is_tag_style:
            return ", ".join(self._translate_segment(s) for s in segments)
        return self._translate_segment(text)

    def _translate_segment(self, text: str) -> str:
        if self.kind == "heavy":
            iso = _detect_iso(text)
            self._tokenizer.src_lang = NLLB_LANG.get(iso, "eng_Latn")
            inputs = self._tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            tgt = self._tokenizer.convert_tokens_to_ids("eng_Latn")
            out = self._model.generate(
                **inputs,
                forced_bos_token_id=tgt,
                max_new_tokens=512,
                num_beams=5,
                no_repeat_ngram_size=3,
            )
        else:
            inputs = self._tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            out = self._model.generate(
                **inputs,
                max_new_tokens=512,
                num_beams=5,
                no_repeat_ngram_size=3,
            )
        return self._tokenizer.decode(out[0], skip_special_tokens=True)
