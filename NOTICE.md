# Third-party model notices

The source code in this repository is licensed under MIT (see `LICENSE`).
However, this project depends on pretrained model weights distributed by their
respective authors. **Model weights are NOT included in this repository** —
they are downloaded on first run from HuggingFace into the local `hf-cache/`
directory by the user.

The licenses below govern the use of those model weights, not this source code.
You must comply with each model's license when using it.

---

## Stable Audio Open 1.0

- **Repo:** https://huggingface.co/stabilityai/stable-audio-open-1.0
- **License:** Stability AI Community License Agreement
- **License text:** https://stability.ai/license
- **Acceptance required:** yes — you must visit the model page and click
  "Agree and access repository" before download will succeed
- **Allowed use (summary, not legal advice):**
  - Free for individuals and organizations with annual revenue under $1M USD
  - Above that threshold, an Enterprise license from Stability AI is required
  - Attribution required: outputs and derivative works should credit
    "Powered by Stable Audio Open 1.0"
  - You must pass the license through to anyone you redistribute the model to

A copy of the license is bundled with the model weights, at:
`hf-cache/hub/models--stabilityai--stable-audio-open-1.0/snapshots/<hash>/LICENSE.md`

---

## Helsinki-NLP/opus-mt-mul-en  (light translator option)

- **Repo:** https://huggingface.co/Helsinki-NLP/opus-mt-mul-en
- **License:** Apache 2.0
- **Allowed use:** broad, including commercial — see Apache-2.0 terms
- **Citation:**
  > Tiedemann, J. (2020). "The Tatoeba Translation Challenge — Realistic Data
  > Sets for Low Resource and Multilingual MT", in Proc. of WMT 2020.

---

## facebook/nllb-200-distilled-600M  (heavy translator option)

- **Repo:** https://huggingface.co/facebook/nllb-200-distilled-600M
- **License:** CC-BY-NC 4.0
- **Allowed use:** **NON-COMMERCIAL ONLY**
- **Citation:**
  > NLLB Team et al. (2022). "No Language Left Behind: Scaling Human-Centered
  > Machine Translation", arXiv:2207.04672.

⚠️ **Commercial-use warning:** if you plan to use this software commercially,
choose the `light` translator option (opus-mt-mul-en, Apache 2.0). The `heavy`
option (NLLB) is restricted to non-commercial use.

---

## Python libraries

This project uses the following libraries via `requirements.txt`:

| Library | License |
| --- | --- |
| diffusers | Apache 2.0 |
| transformers | Apache 2.0 |
| accelerate | Apache 2.0 |
| huggingface_hub | Apache 2.0 |
| torch / torchaudio | BSD-3-Clause |
| gradio | Apache 2.0 |
| sentencepiece | Apache 2.0 |
| protobuf | BSD-3-Clause |
| soundfile | BSD-3-Clause |
| numpy | BSD-3-Clause |
| torchsde | Apache 2.0 |

All are permissive licenses compatible with this project's MIT license.
