**언어:**
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

## 빠른 시작

0. [Download Last Release](https://github.com/oscarlumiere/Stable-Audio-Insight/releases/latest)
1. https://huggingface.co 에서 회원가입 (계정이 있으면 건너뛰기)
2. https://huggingface.co/stabilityai/stable-audio-open-1.0 을 열고 **Agree and access repository** 클릭
3. https://huggingface.co/settings/tokens 에서 **New token** → Type: Read → Create
4. `install.bat` 실행 → 언어 선택 → 토큰 붙여넣기 → 번역기 선택. 완료.

그 다음 `run.bat` 으로 http://127.0.0.1:7860 가 열립니다.


Stability AI 의 [Stable Audio Open 1.0](https://huggingface.co/stabilityai/stable-audio-open-1.0) 를 위한 독립형 Windows 앱. 사운드 디자인, 게임 오디오, 영상 편집, 음악 스케치를 위해 제작.

## 포함된 기능

- **9 개 언어 UI** (English, Русский, 中文, 日本語, Español, Français, Deutsch, Português, 한국어) — Gradio 푸터의 전환기로 즉시 변경
- **다국어 프롬프트** — 키릴 / CJK / 아랍 / 히브리 / 그리스 / 태국 / 데바나가리 입력 시 생성 전에 자동으로 영어로 번역. 설치 시 `opus-mt-mul-en` (light, ~300 MB) 또는 `nllb-200-distilled-600M` (heavy, ~2.4 GB) 중 선택
- **약 217 개 프리셋, 15 개 카테고리** — 발걸음, 충격, 동작, UI, 무기, 앰비언스, 차량, 자연, 음악, 시네마틱, 마법, SF, 호러, 동물, 군중과 목소리
- **다중 변형 생성** — 클릭당 1~4 개 (`num_waveforms_per_prompt`), 스케줄러 선택 (Default / DPM++ 2M / Euler), 무작위 seed 버튼, Re-roll 버튼
- **세션 기록** — 최근 10 회 생성을 접을 수 있는 미니 플레이어로 표시
- **배치 모드** — 줄당 하나씩 프롬프트 입력, 각각 `outputs/Saved/` 에 바로 저장
- **ZIP 내보내기** — `outputs/Saved/` 를 한 번에 압축
- **게임 친화적 출력** — slug 파일명 (`wood_floor_footsteps_01.wav`), 폴더별 자동 번호 매김; WAV INFO 청크 메타데이터에 전체 프롬프트, seed, 길이, steps, cfg, 샘플레이트, negative 기록 — Reaper, Audition, Ableton, ffprobe 에서 읽힘
- **GPU/CPU 실시간 전환** 및 저용량 VRAM 용 `RunOnCPU.bat`
- **세션 로그** — `logs/app-YYYYMMDD-HHMMSS.log` 에 오류 시 전체 트레이스백 기록
- **단일 파일 설치 프로그램** (`install.bat`) — Python 3.11.9 를 프로젝트 폴더 내에 자동 설치, `nvidia-smi` 로 `torch+cu128` 또는 CPU torch 선택, 모델과 번역기 다운로드. 진정한 휴대성: 폴더 삭제 시 시스템에 흔적 없음
- **업데이트** — `update.bat` 가 종속성을 새로 고치고 모델을 재동기화

## 시스템 요구 사항

- Windows 10 / 11 (Windows 11 Pro 에서 테스트)
- Python **3.11.x** — https://www.python.org/downloads/release/python-3119/
  (설치 시 **Add Python to PATH** 선택)
- CUDA 12.x 지원 NVIDIA GPU:
  - **최소**: ~4 GB VRAM (fp16, 1 변형, ≤ 20 초, ≤ 100 스텝)
  - **권장**: 8 GB+ VRAM, 4 변형 × 47 초, 100+ 스텝 기준
  - 6 GB 는 1–2 변형은 안정적; 4 변형 동시에는 OOM 가능
  - 다른 CUDA 버전은 `install.bat` / `setup.bat` 의 PyTorch 인덱스를
    변경 (예: CUDA 12.1 → `cu121`)
  - NVIDIA 없음 → `RunOnCPU.bat` 또는 UI 의 **GPU/CPU** 토글 사용
    (느리지만 작동)
- **설치 시 15–20 GB 여유 공간** (설치 후 상주 약 10–13 GB):
  - ~5 GB — Stable Audio Open 가중치
  - ~4–5 GB — Python + PyTorch CUDA + 의존성
  - 0.3–2.4 GB — 번역기 (선택에 따라)
  - ~5 GB — HuggingFace 및 pip 캐시 + 설치 임시 파일 (대부분 나중에 정리 가능)
- HuggingFace 계정 + read 토큰 (최초 다운로드 시에만 필요)

## HuggingFace 토큰이 필요한가요?

**한 번만 — Stable Audio 가중치 다운로드 용도로만 필요합니다.** 이후
앱은 로컬 캐시 `hf-cache/` 에서 오프라인으로 동작합니다.

Stable Audio Open 1.0 은 *gated* 모델 — Stability AI 가 등록 계정과
라이선스 동의를 요구합니다. 따라서:

1. https://huggingface.co 에서 계정 가입 (없다면)
2. 모델 페이지를 열고 **라이선스에 동의**:
   https://huggingface.co/stabilityai/stable-audio-open-1.0
   (**Agree and access repository** 클릭 — 안 하면 다운로드가
   403 을 반환)
3. read 토큰 발급: https://huggingface.co/settings/tokens
4. `install.bat` 실행 중 적절한 시점에 토큰을 묻습니다

번역 모델(`opus-mt-mul-en`, `nllb-200-distilled-600M`)은 토큰이
**필요 없습니다** — 공개 모델입니다.

## 설치 (권장 방법)

한 파일이 모든 것을 처리합니다:

```
install.bat
```

수행 단계:

1. 안내 메시지 언어 선택 (1–9: 영어, 러시아어, 중국어, 일본어,
   스페인어, 프랑스어, 독일어, 포르투갈어, 한국어)
2. PATH 의 Python 3.11 확인 (`py -3.11`)
3. `.venv` 생성, pip / wheel 업그레이드
4. PyTorch (CUDA 12.8) 와 `requirements.txt` 의 나머지 의존성 설치
5. HF 토큰 입력 요청 (이미 로그인 시 건너뜀)
6. **번역 모델 선택을 묻습니다:**
   - **1. LIGHT** — `Helsinki-NLP/opus-mt-mul-en`
     - ~300 MB, 빠름, Apache 2.0 (상업적 사용 가능)
     - 보통 품질, 음악 용어를 가끔 잘못 번역
   - **2. HEAVY** — `facebook/nllb-200-distilled-600M`
     - ~2.4 GB, 더 느림, CC-BY-NC 4.0 (**비상업적 사용만**)
     - 더 높은 품질, 영어가 아닌 언어에 권장
7. 선택을 `hf-cache/translator.cfg` 에 저장
8. Stable Audio (~5 GB) 와 선택한 번역기를 `hf-cache/` 에 다운로드

## 실행

```
run.bat
```

브라우저 탭이 http://127.0.0.1:7860 에서 열립니다.

## 설치 후 번역기 변경

가장 빠른 방법:

1. `hf-cache/translator.cfg` 를 열어 `light` 또는 `heavy` 로 변경
2. `download.bat` 실행 — 캐시에 없으면 선택된 모델을 다운로드
3. `run.bat`

또는 `hf-cache/translator.cfg` 를 삭제하고 `install.bat` 을 다시 실행 — 다시
묻지만, 의존성과 Stable Audio 는 이미 캐시되어 재다운로드되지 않습니다.

## 단계별 설치 (문제가 생긴 경우)

`install.bat` 은 네 개의 작은 스크립트를 묶은 것이며, 각각 단독 실행
가능합니다:

| 스크립트 | 역할 |
| --- | --- |
| `setup.bat` | `.venv` 생성 및 의존성 설치 |
| `login.bat` | HuggingFace 인증 (`hf auth login`) |
| `download.bat` | `hf-cache/translator.cfg` 기반으로 Stable Audio + 번역기 다운로드 |
| `run.bat` | Gradio 웹 UI 실행 |

## 프로젝트 구조

```
.
├── app.py              # Gradio UI + 생성
├── translator.py       # 번역 모듈 (light / heavy)
├── download_model.py   # HuggingFace 모델 다운로드
├── requirements.txt    # Python 의존성
├── install.bat         # 단일 인스톨러 (다국어)
├── setup.bat           # venv + 의존성만
├── login.bat           # HF 인증만
├── download.bat        # 다운로드만
├── run.bat             # 웹 UI 실행
├── hf-cache/translator.cfg  # light / heavy (install.bat 이 생성)
├── README.md           # main docs (English)
├── docs/i18n/          # localized versions (8 languages)
├── LICENSE             # MIT — 본 저장소 소스 코드
├── NOTICE.md           # 사용된 모델들의 라이선스
├── hf-cache/           # 로컬 HF 캐시 (git 에 포함 안 됨)
└── outputs/            # 저장된 오디오 (git 에 포함 안 됨)
    ├── intermediate/   # "Save all" 체크 시
    └── Saved/          # "Save" 버튼 누를 때
```

## 환경 변수

`run.bat` 실행 전에 설정 가능:

| 변수 | 기본값 | 용도 |
| --- | --- | --- |
| `HOST` | `127.0.0.1` | Gradio 호스트 |
| `PORT` | `7860` | Gradio 포트 |
| `SHARE` | `0` | `1` 이면 공개 gradio.live URL 생성 |
| `STABLE_AUDIO_MODEL` | `stabilityai/stable-audio-open-1.0` | 모델 변경 |

## 라이선스

본 저장소의 **소스 코드** — MIT (`LICENSE` 참고).

**모델**들은 각자의 라이선스를 따릅니다 (전문은 `NOTICE.md`):

| 모델 | 라이선스 | 상업적 사용 |
| --- | --- | --- |
| Stable Audio Open 1.0 | Stability AI Community | 연 매출 100 만 달러 이하: 가능, 초과 시 Enterprise |
| opus-mt-mul-en (light) | Apache 2.0 | 가능 |
| NLLB-200-distilled-600M (heavy) | CC-BY-NC 4.0 | **불가, 비상업적 사용만** |

상업적 사용 예정이면 설치 시 **light** 를 선택하세요.

## 테스트 환경

- Windows 11 Pro
- Python 3.11.9
- NVIDIA RTX 5080 (16 GB VRAM)
- CUDA 12.8
- PyTorch 2.11.0+cu128

## 크레딧

- **[Stable Audio Open 1.0](https://huggingface.co/stabilityai/stable-audio-open-1.0)** — Stability AI
- **[opus-mt-mul-en](https://huggingface.co/Helsinki-NLP/opus-mt-mul-en)** — Helsinki-NLP / Tatoeba Translation Challenge
- **[NLLB-200](https://huggingface.co/facebook/nllb-200-distilled-600M)** — Meta AI / FAIR
- **[Gradio](https://github.com/gradio-app/gradio)**, **[diffusers](https://github.com/huggingface/diffusers)**, **[transformers](https://github.com/huggingface/transformers)**, **[accelerate](https://github.com/huggingface/accelerate)** — HuggingFace
- **래퍼 개발** — [Oscar Lumiere](https://www.io-oscar.com/)
- **지원** — [Claude Code](https://www.anthropic.com/claude-code) (Anthropic)
