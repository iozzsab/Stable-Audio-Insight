**言語:**
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

## クイックスタート

1. https://huggingface.co で登録（既にアカウントがあればスキップ）
2. https://huggingface.co/stabilityai/stable-audio-open-1.0 を開いて **Agree and access repository** をクリック
3. https://huggingface.co/settings/tokens で **New token** → Type: Read → Create
4. `install.bat` を実行 → UI 言語選択 → トークン貼付 → 翻訳器選択。完了。

その後 `run.bat` で http://127.0.0.1:7860 が開きます。


Stability AI の [Stable Audio Open 1.0](https://huggingface.co/stabilityai/stable-audio-open-1.0) のための自己完結型 Windows アプリ。サウンドデザイン、ゲームオーディオ、動画編集、音楽スケッチ用に設計。

## 機能一覧

- **UI 9 言語**（English / Русский / 中文 / 日本語 / Español / Français / Deutsch / Português / 한국어）— Gradio フッターの切替器でリアルタイム切替
- **多言語プロンプト** — キリル / CJK / アラビア / ヘブライ / ギリシャ / タイ / デーヴァナーガリーで入力すると、生成前に自動的に英訳。インストール時に `opus-mt-mul-en`（軽量、約300 MB）または `nllb-200-distilled-600M`（高品質、約2.4 GB）を選択
- **約 217 のプリセット（15 カテゴリ）** — 足音、衝撃、動作、UI、武器、環境音、乗り物、自然、音楽、シネマティック、魔法、SF、ホラー、動物、群衆と声
- **マルチバリエーション生成** — 1 クリックで 1〜4 個生成（`num_waveforms_per_prompt`）、スケジューラ選択（Default / DPM++ 2M / Euler）、ランダム seed ボタン、Re-roll ボタン
- **セッション履歴** — 直近 10 件をミニプレイヤー付きアコーディオンで表示
- **バッチモード** — 1 行 1 プロンプトでリスト指定、それぞれ `outputs/Saved/` に直接保存
- **ZIP エクスポート** — `outputs/Saved/` をワンクリックで圧縮
- **ゲーム向け出力** — スラグファイル名（`wood_floor_footsteps_01.wav`）にフォルダ別連番、WAV INFO チャンクに完全プロンプト・seed・長さ・steps・cfg・サンプルレート・negative を埋め込み、Reaper / Audition / Ableton / ffprobe で読み取れます
- **GPU/CPU 切替**（低 VRAM 用 `RunOnCPU.bat` あり）
- **セッションログ** — `logs/app-YYYYMMDD-HHMMSS.log` にエラー時のフルトレースバックを記録
- **ワンファイルインストーラ**（`install.bat`）— Python 3.11.9 をプロジェクトフォルダ内にサイレントインストール、`nvidia-smi` で `torch+cu128` か CPU torch を自動選択、モデルと翻訳器をダウンロード。フォルダごと削除すればシステムに痕跡ゼロ
- **アップデート** — `update.bat` で依存関係とモデルを更新

## システム要件

- Windows 10 / 11（Windows 11 Pro でテスト）
- Python **3.11.x** — https://www.python.org/downloads/release/python-3119/
  （インストール時に **Add Python to PATH** をチェック）
- CUDA 12.x 対応の NVIDIA GPU:
  - **最小**: ~4 GB VRAM（fp16、1 バリエーション、≤ 20 秒、≤ 100 ステップ）
  - **推奨**: 8 GB 以上の VRAM（4 バリエーション × 47 秒、100+ ステップ向け）
  - 6 GB は 1–2 バリエーションで快適。4 バリエーション同時は OOM の可能性
  - 別の CUDA バージョンの場合は `install.bat` / `setup.bat` の PyTorch
    インデックスを変更（例: CUDA 12.1 → `cu121`）
  - NVIDIA カードが無い → `RunOnCPU.bat` または UI 上の **GPU/CPU**
    トグルを使用（遅いが動作します）
- **インストール時に 15–20 GB の空き容量**（インストール後の常駐は約 10–13 GB）:
  - ~5 GB — Stable Audio Open のウェイト
  - ~4–5 GB — Python + PyTorch CUDA + 依存関係
  - 0.3–2.4 GB — 翻訳モデル（選択次第）
  - ~5 GB — HuggingFace と pip のキャッシュ + インストール一時ファイル（多くはあとで削除可能）
- HuggingFace アカウント + read トークン（初回ダウンロード時のみ）

## HuggingFace トークンは必要？

**初回 1 回のみ — Stable Audio のウェイトをダウンロードするためだけに必要**
です。それ以降はローカルキャッシュ `hf-cache/` からオフラインで動作します。

Stable Audio Open 1.0 は *gated*（ゲート付き）モデル — Stability AI は
登録アカウントとライセンス同意を要求します。手順：

1. https://huggingface.co でアカウント登録（未登録の場合）
2. モデルページで**ライセンスに同意**：
   https://huggingface.co/stabilityai/stable-audio-open-1.0
   （**Agree and access repository** をクリック — これがないと
   ダウンロードは 403 になります）
3. read トークンを発行：https://huggingface.co/settings/tokens
4. `install.bat` が適切なタイミングでトークン入力を求めます

翻訳モデル（`opus-mt-mul-en` と `nllb-200-distilled-600M`）にはトークンは
**不要**です。公開モデルです。

## インストール（推奨）

1 ファイルですべて完了：

```
install.bat
```

実行内容：

1. プロンプト言語を選択（1–9: 英、露、中、日、西、仏、独、葡、韓）
2. PATH 上の Python 3.11 を確認（`py -3.11`）
3. `.venv` を作成、pip / wheel をアップグレード
4. PyTorch (CUDA 12.8) と `requirements.txt` の依存関係をインストール
5. HF トークンを尋ねる（既にログイン済みならスキップ可）
6. **どちらの翻訳モデルをインストールするか質問：**
   - **1. LIGHT** — `Helsinki-NLP/opus-mt-mul-en`
     - 約300 MB、高速、Apache 2.0（商用OK）
     - 品質は中程度、音楽用語で誤訳することあり
   - **2. HEAVY** — `facebook/nllb-200-distilled-600M`
     - 約2.4 GB、低速、CC-BY-NC 4.0（**非商用のみ**）
     - 高品質、英語以外には推奨
7. 選択を `hf-cache/translator.cfg` に保存
8. Stable Audio (~5 GB) と選択した翻訳モデルを `hf-cache/` にダウンロード

## 起動

```
run.bat
```

ブラウザが http://127.0.0.1:7860 を開きます。

## インストール後に翻訳モデルを切り替える

最も簡単な方法：

1. `hf-cache/translator.cfg` を `light` または `heavy` に変更
2. `download.bat` を実行 — キャッシュにない場合のみダウンロード
3. `run.bat`

または `hf-cache/translator.cfg` を削除して再度 `install.bat` を実行 — 再質問しますが、
依存関係と Stable Audio はキャッシュ済みなので再ダウンロードしません。

## ステップごとのインストール（問題が出たとき）

`install.bat` は 4 つの小さなスクリプトをまとめたものです。個別に実行可能：

| スクリプト | 役割 |
| --- | --- |
| `setup.bat` | `.venv` 作成と依存関係インストール |
| `login.bat` | HuggingFace 認証（`hf auth login`） |
| `download.bat` | `hf-cache/translator.cfg` の指定で Stable Audio + 翻訳モデルをダウンロード |
| `run.bat` | Gradio Web UI を起動 |

## プロジェクト構成

```
.
├── app.py              # Gradio UI + 生成
├── translator.py       # 翻訳モジュール (light / heavy)
├── download_model.py   # HuggingFace モデルダウンロード
├── requirements.txt    # Python 依存関係
├── install.bat         # 一括インストーラー（多言語）
├── setup.bat           # venv + 依存関係のみ
├── login.bat           # HF 認証のみ
├── download.bat        # ダウンロードのみ
├── run.bat             # Web UI 起動
├── hf-cache/translator.cfg  # light / heavy（install.bat が作成）
├── README.md           # main docs (English)
├── docs/i18n/          # localized versions (8 languages)
├── LICENSE             # MIT — 本リポジトリのソースコード
├── NOTICE.md           # 使用モデルのライセンス
├── hf-cache/           # ローカル HF キャッシュ（git に入れない）
└── outputs/            # 保存した音声（git に入れない）
    ├── intermediate/   # "Save all" チェック時
    └── Saved/          # "Save" ボタン押下時
```

## 環境変数

`run.bat` 実行前に上書き可能：

| 変数 | デフォルト | 用途 |
| --- | --- | --- |
| `HOST` | `127.0.0.1` | Gradio ホスト |
| `PORT` | `7860` | Gradio ポート |
| `SHARE` | `0` | `1` で公開 gradio.live URL を生成 |
| `STABLE_AUDIO_MODEL` | `stabilityai/stable-audio-open-1.0` | モデル変更 |

## ライセンス

本リポジトリの**ソースコード** — MIT（`LICENSE` 参照）。

**モデル**はそれぞれ独自のライセンス（全文は `NOTICE.md`）：

| モデル | ライセンス | 商用利用 |
| --- | --- | --- |
| Stable Audio Open 1.0 | Stability AI Community | 年商 100 万ドル以下：可、超過時はエンタープライズ |
| opus-mt-mul-en (light) | Apache 2.0 | 可 |
| NLLB-200-distilled-600M (heavy) | CC-BY-NC 4.0 | **不可（非商用のみ）** |

商用利用予定なら、インストール時に **light** を選んでください。

## テスト環境

- Windows 11 Pro
- Python 3.11.9
- NVIDIA RTX 5080 (16 GB VRAM)
- CUDA 12.8
- PyTorch 2.11.0+cu128

## クレジット

- **Stable Audio Open 1.0** — Stability AI
- **opus-mt-mul-en** — Helsinki-NLP / Tatoeba Translation Challenge
- **NLLB-200** — Meta AI / FAIR
- **Gradio**、**diffusers**、**transformers**、**accelerate** — HuggingFace
- **ラッパー開発** — Oscar Lumiere
- **支援** — [Claude Code](https://www.anthropic.com/claude-code) (Anthropic)
