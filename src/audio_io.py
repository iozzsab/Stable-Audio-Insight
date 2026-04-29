import re
import struct
from pathlib import Path

import numpy as np
import soundfile as sf


def slugify_prompt(prompt: str, max_words: int = 4) -> str:
    words = re.findall(r"[A-Za-z0-9]+", prompt.lower())[:max_words]
    return "_".join(words) if words else "audio"


def next_counter(directory: Path, slug: str) -> int:
    pattern = re.compile(rf"^{re.escape(slug)}_(\d+)\.wav$", re.IGNORECASE)
    used: list[int] = []
    if directory.exists():
        for f in directory.iterdir():
            m = pattern.match(f.name)
            if m:
                used.append(int(m.group(1)))
    return (max(used) + 1) if used else 1


def post_audio(audio) -> np.ndarray:
    if hasattr(audio, "cpu"):
        audio = audio.cpu().numpy()
    audio = np.asarray(audio, dtype=np.float32)
    if audio.ndim == 2 and audio.shape[0] in (1, 2):
        audio = audio.T
    peak = np.max(np.abs(audio))
    if peak > 1.0:
        audio = audio / peak
    return audio


_TAG_MAP = {
    "title": b"INAM",
    "artist": b"IART",
    "comment": b"ICMT",
    "software": b"ISFT",
    "creation_date": b"ICRD",
}


def write_wav_with_metadata(path: Path, audio: np.ndarray, sample_rate: int, info: dict[str, str]) -> None:
    sf.write(str(path), audio, sample_rate)
    if not info:
        return
    with open(path, "rb") as f:
        data = f.read()
    info_data = b""
    for key, value in info.items():
        tag = _TAG_MAP.get(key)
        if not tag or not value:
            continue
        v = value.encode("utf-8") + b"\x00"
        if len(v) % 2:
            v += b"\x00"
        info_data += tag + struct.pack("<I", len(v)) + v
    if not info_data:
        return
    list_chunk = b"LIST" + struct.pack("<I", 4 + len(info_data)) + b"INFO" + info_data
    new_data = data + list_chunk
    new_riff_size = len(new_data) - 8
    new_data = new_data[:4] + struct.pack("<I", new_riff_size) + new_data[8:]
    with open(path, "wb") as f:
        f.write(new_data)
