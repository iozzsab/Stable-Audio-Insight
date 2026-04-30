**语言:**
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

## 快速开始

0. [Download Last Release](https://github.com/oscarlumiere/Stable-Audio-Insight/releases/latest)
1. 在 https://huggingface.co 注册（如已注册请跳过）
2. 打开 https://huggingface.co/stabilityai/stable-audio-open-1.0 → 点击 **Agree and access repository**
3. 在 https://huggingface.co/settings/tokens → **New token** → Type: Read → Create
4. 运行 `install.bat` → 选择 UI 语言 → 粘贴令牌 → 选择翻译器。完成。

然后 `run.bat` 打开 http://127.0.0.1:7860。


面向 [Stable Audio Open 1.0](https://huggingface.co/stabilityai/stable-audio-open-1.0)（Stability AI）的独立 Windows 应用。为音效设计、游戏音频、视频剪辑和音乐草稿而生。

## 内含功能

- **9 种 UI 语言**（English / Русский / 中文 / 日本語 / Español / Français / Deutsch / Português / 한국어），Gradio 页脚切换器即时切换
- **多语言提示** — 西里尔 / CJK / 阿拉伯 / 希伯来 / 希腊 / 泰 / 天城文输入，自动翻译为英语后再生成。安装时可选 `opus-mt-mul-en`（轻量，~300 MB）或 `nllb-200-distilled-600M`（高质量，~2.4 GB）
- **约 217 个预设，分 15 大类** — 脚步、撞击、动作、UI、武器、氛围、载具、自然、音乐、电影、魔法、科幻、恐怖、动物、人群与声音
- **多变体生成** — 一次生成 1–4 个（`num_waveforms_per_prompt`），调度器选择（Default / DPM++ 2M / Euler），随机种子按钮，Re-roll 按钮
- **会话历史** — 最近 10 次生成以折叠迷你播放器形式展示
- **批量模式** — 多行提示词，每行一条，依次直接保存到 `outputs/Saved/`
- **ZIP 导出** `outputs/Saved/` 一键打包
- **游戏就绪输出** — slug 文件名（`wood_floor_footsteps_01.wav`）带每目录递增编号；WAV INFO 块写入完整提示、seed、时长、steps、cfg、采样率、negative，可在 Reaper / Audition / Ableton / ffprobe 中读取
- **GPU/CPU 实时切换** 以及 `RunOnCPU.bat`（适合低显存设备）
- **会话日志** 写入 `logs/app-YYYYMMDD-HHMMSS.log`，错误带完整堆栈
- **一键安装**（`install.bat`）— 静默把 Python 3.11.9 装到项目文件夹内，根据 `nvidia-smi` 选择 `torch+cu128` 或 CPU torch，下载模型与翻译器。完全便携：删项目即清干净，系统无痕
- **更新流程** — `update.bat` 刷新依赖并同步模型

## 系统要求

- Windows 10 / 11（在 Windows 11 Pro 上测试）
- Python **3.11.x** — https://www.python.org/downloads/release/python-3119/
  （安装时勾选 **Add Python to PATH**）
- 支持 CUDA 12.x 的 NVIDIA 显卡：
  - **最低**：~4 GB VRAM（fp16、1 个变体、≤ 20 秒、≤ 100 步）
  - **推荐**：8 GB+ VRAM，用于 4 个变体 × 47 秒、100+ 步
  - 6 GB 可正常运行 1–2 个变体；4 个同时变体可能 OOM
  - 其他 CUDA 版本请修改 `install.bat` / `setup.bat` 中的 PyTorch 索引
    （例如 CUDA 12.1 用 `cu121`）
  - 无 NVIDIA 显卡 → 使用 `RunOnCPU.bat` 或界面中的 **GPU/CPU** 切换
    （较慢但可用）
- **安装时约 15–20 GB 可用磁盘空间**（安装后常驻约 10–13 GB）：
  - ~5 GB — Stable Audio Open 权重
  - ~4–5 GB — Python + PyTorch CUDA + 依赖
  - 0.3–2.4 GB — 翻译器（按选择）
  - ~5 GB — HuggingFace + pip 缓存 + 安装时临时文件（大多数可后续清理）
- HuggingFace 账号 + read 令牌（仅初次下载需要）

## 是否需要 HuggingFace 令牌？

**只需一次 — 仅用于下载 Stable Audio 权重。** 之后应用直接从本地
`hf-cache/` 离线运行。

Stable Audio Open 1.0 是 *gated*（受限）模型 — Stability AI 要求注册账号
并接受许可协议后才能下载。所以：

1. 在 https://huggingface.co 注册账号（如尚未注册）
2. 打开模型页面并**接受许可**：
   https://huggingface.co/stabilityai/stable-audio-open-1.0
   （点击 **Agree and access repository**，否则下载返回 403）
3. 创建 read 令牌：https://huggingface.co/settings/tokens
4. `install.bat` 会在合适的时候让您粘贴令牌

翻译模型（`opus-mt-mul-en` 和 `nllb-200-distilled-600M`）**不需要**令牌
— 它们是公开模型。

## 安装（推荐方式）

一个文件搞定全部：

```
install.bat
```

它会：

1. 选择安装提示语言（1–9：英、俄、中、日、西、法、德、葡、韩）
2. 检查 PATH 中是否有 Python 3.11（`py -3.11`）
3. 创建 `.venv` 并升级 pip / wheel
4. 安装 PyTorch (CUDA 12.8) 和 `requirements.txt` 中其余依赖
5. 询问 HF 令牌（如已登录可跳过）
6. **询问要安装哪个翻译器：**
   - **1. LIGHT** — `Helsinki-NLP/opus-mt-mul-en`
     - ~300 MB，速度快，Apache 2.0（允许商用）
     - 中等质量，音乐术语有时翻错
   - **2. HEAVY** — `facebook/nllb-200-distilled-600M`
     - ~2.4 GB，慢一些，CC-BY-NC 4.0（**仅限非商业**）
     - 更高质量，推荐用于非英语
7. 选择保存到 `hf-cache/translator.cfg`
8. 下载 Stable Audio (~5 GB) 和所选翻译器到 `hf-cache/`

## 运行

```
run.bat
```

浏览器会自动打开 http://127.0.0.1:7860。

## 安装后切换翻译器

最简单的方式：

1. 打开 `hf-cache/translator.cfg` 改为 `light` 或 `heavy`
2. 运行 `download.bat` — 缓存中没有时会下载选中的
3. `run.bat`

或者删除 `hf-cache/translator.cfg` 后重新运行 `install.bat` — 它会再问一次，
依赖和 Stable Audio 已缓存不会重复下载。

## 分步安装（如有问题）

`install.bat` 是四个小脚本的集合，任何一个都可以单独运行：

| 脚本 | 作用 |
| --- | --- |
| `setup.bat` | 创建 `.venv` 并安装依赖 |
| `login.bat` | HuggingFace 认证（`hf auth login`） |
| `download.bat` | 根据 `hf-cache/translator.cfg` 下载 Stable Audio + 翻译器 |
| `run.bat` | 启动 Gradio 网页界面 |

## 项目结构

```
.
├── app.py              # Gradio UI + 生成
├── translator.py       # 翻译器模块 (light / heavy)
├── download_model.py   # 从 HuggingFace 下载模型
├── requirements.txt    # Python 依赖
├── install.bat         # 一键安装器（多语言）
├── setup.bat           # 仅创建 venv + 安装依赖
├── login.bat           # 仅 HF 认证
├── download.bat        # 仅下载模型
├── run.bat             # 启动 Web UI
├── hf-cache/translator.cfg  # light / heavy（由 install.bat 创建）
├── README.md           # main docs (English)
├── docs/i18n/          # localized versions (8 languages)
├── LICENSE             # MIT — 仓库源代码
├── NOTICE.md           # 所用模型的许可
├── hf-cache/           # 本地 HF 缓存（不入 git）
└── outputs/            # 已保存音频（不入 git）
    ├── intermediate/   # "Save all" 复选框开启时
    └── Saved/          # 点击 "Save" 按钮时
```

## 环境变量

可在运行 `run.bat` 前覆盖：

| 变量 | 默认 | 用途 |
| --- | --- | --- |
| `HOST` | `127.0.0.1` | Gradio 主机 |
| `PORT` | `7860` | Gradio 端口 |
| `SHARE` | `0` | `1` 表示创建公开的 gradio.live 链接 |
| `STABLE_AUDIO_MODEL` | `stabilityai/stable-audio-open-1.0` | 覆盖默认模型 |

## 许可

本仓库**源代码** — MIT（见 `LICENSE`）。

**模型**各有自己的许可（完整文本见 `NOTICE.md`）：

| 模型 | 许可 | 商业用途 |
| --- | --- | --- |
| Stable Audio Open 1.0 | Stability AI Community | 年收入 100 万美元以下：可以；以上需企业许可 |
| opus-mt-mul-en (light) | Apache 2.0 | 可以 |
| NLLB-200-distilled-600M (heavy) | CC-BY-NC 4.0 | **不可，仅限非商业** |

商业用途请在安装时选择 **light** 翻译器。

## 测试环境

- Windows 11 Pro
- Python 3.11.9
- NVIDIA RTX 5080 (16 GB VRAM)
- CUDA 12.8
- PyTorch 2.11.0+cu128

## 致谢

- **[Stable Audio Open 1.0](https://huggingface.co/stabilityai/stable-audio-open-1.0)** — Stability AI
- **[opus-mt-mul-en](https://huggingface.co/Helsinki-NLP/opus-mt-mul-en)** — Helsinki-NLP / Tatoeba Translation Challenge
- **[NLLB-200](https://huggingface.co/facebook/nllb-200-distilled-600M)** — Meta AI / FAIR
- **[Gradio](https://github.com/gradio-app/gradio)**、**[diffusers](https://github.com/huggingface/diffusers)**、**[transformers](https://github.com/huggingface/transformers)**、**[accelerate](https://github.com/huggingface/accelerate)** — HuggingFace
- **封装开发** — [Oscar Lumiere](https://www.io-oscar.com/)
- **协助** — [Claude Code](https://www.anthropic.com/claude-code) (Anthropic)
