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

## Início rápido

1. Cadastre-se em https://huggingface.co (pule se já tiver conta)
2. Abra https://huggingface.co/stabilityai/stable-audio-open-1.0 → clique em **Agree and access repository**
3. Em https://huggingface.co/settings/tokens → **New token** → Type: Read → Create
4. Execute `install.bat` → escolha o idioma → cole o token → escolha o tradutor. Pronto.

Depois `run.bat` abre http://127.0.0.1:7860.


Aplicativo Windows autocontido para [Stable Audio Open 1.0](https://huggingface.co/stabilityai/stable-audio-open-1.0) da Stability AI. Feito para sound design, áudio de jogos, edição de vídeo e esboços musicais.

## O que inclui

- **UI em 9 idiomas** (English, Русский, 中文, 日本語, Español, Français, Deutsch, Português, 한국어) — seletor no rodapé do Gradio troca tudo na hora
- **Prompts multilíngues** — escreva em cirílico / CJK / árabe / hebraico / grego / tailandês / devanágari, tradução automática para inglês antes da geração. Duas opções na instalação: `opus-mt-mul-en` (light, ~300 MB) ou `nllb-200-distilled-600M` (heavy, ~2.4 GB)
- **~217 presets em 15 categorias** — Passos, Impactos, Movimento, UI, Armas, Ambiente, Veículos, Natureza, Música, Cinemático, Magia, Sci-Fi, Horror, Animais, Multidão e voz
- **Geração de múltiplas variações** — 1 a 4 áudios por clique (`num_waveforms_per_prompt`), seletor de scheduler (Default / DPM++ 2M / Euler), botão de seed aleatório, botão Re-roll
- **Histórico de sessão** — últimas 10 gerações como mini-players retráteis
- **Modo em lote** — cole muitos prompts (um por linha), cada um salvo direto em `outputs/Saved/`
- **Exportar ZIP** de `outputs/Saved/` com um clique
- **Saída game-ready** — nomes slug (`wood_floor_footsteps_01.wav`) com contador por pasta; metadados WAV INFO com prompt completo, seed, duração, steps, cfg, sample rate, negative — lidos por Reaper, Audition, Ableton, ffprobe
- **Alternância GPU/CPU ao vivo** e `RunOnCPU.bat` para sistemas com pouca VRAM
- **Log por sessão** em `logs/app-YYYYMMDD-HHMMSS.log` com tracebacks completos em erros
- **Instalador de um arquivo** (`install.bat`) — instala Python 3.11.9 silenciosamente dentro do projeto, escolhe `torch+cu128` ou CPU torch via `nvidia-smi`, baixa modelo e tradutor. Verdadeiramente portátil: apagar a pasta não deixa rastros
- **Atualização** — `update.bat` atualiza dependências e ressincroniza modelos

## Requisitos

- Windows 10 / 11 (testado no Windows 11 Pro)
- Python **3.11.x** — https://www.python.org/downloads/release/python-3119/
  (durante a instalação marque **Add Python to PATH**)
- GPU NVIDIA com CUDA 12.8 (testado em RTX 5080, 16 GB VRAM).
  Para outras GPUs altere o índice PyTorch em `install.bat` / `setup.bat`
  (por exemplo `cu121` para CUDA 12.1).
- **15–20 GB livres durante a instalação** (depois: ~10–13 GB residentes):
  - ~5 GB — pesos Stable Audio Open
  - ~4–5 GB — Python + PyTorch CUDA + dependências
  - 0,3–2,4 GB — tradutor (à sua escolha)
  - ~5 GB — caches HuggingFace e pip + arquivos temporários de instalação (a maior parte recuperável depois)
- Conta HuggingFace + token de leitura (apenas para o download inicial)

## Preciso de um token HuggingFace?

**Apenas uma vez — só para baixar os pesos do Stable Audio.** Depois disso o
app funciona offline a partir do cache local `hf-cache/`.

Stable Audio Open 1.0 é um modelo *gated* — a Stability AI exige conta
registrada e aceitação da licença antes do download. Portanto:

1. Registre-se em https://huggingface.co (se ainda não tiver conta)
2. Abra a página do modelo e **aceite a licença**:
   https://huggingface.co/stabilityai/stable-audio-open-1.0
   (clique em **Agree and access repository** — sem isso o download
   retorna 403)
3. Crie um token de leitura: https://huggingface.co/settings/tokens
4. `install.bat` pedirá o token no momento certo

Os tradutores (`opus-mt-mul-en` e `nllb-200-distilled-600M`) **não**
precisam de token — são modelos públicos.

## Instalação (recomendada)

Um único arquivo faz tudo:

```
install.bat
```

O que ele faz:

1. Pergunta o idioma das mensagens (1–9: inglês, russo, chinês, japonês,
   espanhol, francês, alemão, português, coreano)
2. Verifica se Python 3.11 está em PATH (`py -3.11`)
3. Cria `.venv` e atualiza pip / wheel
4. Instala PyTorch (CUDA 12.8) e o resto de `requirements.txt`
5. Pede o token HF (ou pula se já estiver logado)
6. **Pergunta qual tradutor instalar:**
   - **1. LIGHT** — `Helsinki-NLP/opus-mt-mul-en`
     - ~300 MB, rápido, Apache 2.0 (uso comercial OK)
     - Qualidade média, às vezes erra termos musicais
   - **2. HEAVY** — `facebook/nllb-200-distilled-600M`
     - ~2,4 GB, mais lento, CC-BY-NC 4.0 (**apenas não comercial**)
     - Maior qualidade, recomendado para idiomas não ingleses
7. Salva a escolha em `hf-cache/translator.cfg`
8. Baixa Stable Audio (~5 GB) e o tradutor escolhido em `hf-cache/`

## Executar

```
run.bat
```

Abre uma aba em http://127.0.0.1:7860.

## Trocar tradutor após instalação

Caminho rápido:

1. Abra `hf-cache/translator.cfg` e troque para `light` ou `heavy`
2. Execute `download.bat` — baixa o escolhido se não estiver no cache
3. `run.bat`

Ou exclua `hf-cache/translator.cfg` e execute `install.bat` de novo — pergunta
novamente sem rebaixar dependências ou Stable Audio (já em cache).

## Instalação passo a passo (se algo der errado)

`install.bat` envolve quatro scripts menores; cada um pode rodar isolado:

| Script | Função |
| --- | --- |
| `setup.bat` | Cria `.venv` e instala dependências |
| `login.bat` | Autenticação HuggingFace (`hf auth login`) |
| `download.bat` | Baixa Stable Audio + tradutor de `hf-cache/translator.cfg` |
| `run.bat` | Inicia a UI web Gradio |

## Estrutura do projeto

```
.
├── app.py              # UI Gradio + geração
├── translator.py       # Módulo do tradutor (light / heavy)
├── download_model.py   # Downloads dos modelos do HuggingFace
├── requirements.txt    # Dependências Python
├── install.bat         # Instalador único (multilíngue)
├── setup.bat           # Apenas venv + dependências
├── login.bat           # Apenas auth HF
├── download.bat        # Apenas downloads
├── run.bat             # Inicia a UI web
├── hf-cache/translator.cfg  # light / heavy (criado pelo install.bat)
├── README.md           # main docs (English)
├── docs/i18n/          # localized versions (8 languages)
├── LICENSE             # MIT — código fonte do repo
├── NOTICE.md           # Licenças dos modelos usados
├── hf-cache/           # Cache HF local (NÃO no git)
└── outputs/            # Áudio salvo (NÃO no git)
    ├── intermediate/   # Quando "Save all" está marcado
    └── Saved/          # Após clicar em "Save"
```

## Variáveis de ambiente

Defina antes de `run.bat`:

| Variável | Padrão | Função |
| --- | --- | --- |
| `HOST` | `127.0.0.1` | Host Gradio |
| `PORT` | `7860` | Porta Gradio |
| `SHARE` | `0` | `1` = criar link público gradio.live |
| `STABLE_AUDIO_MODEL` | `stabilityai/stable-audio-open-1.0` | Trocar modelo |

## Licenças

O **código fonte** é MIT (veja `LICENSE`).

Os **modelos** têm licenças próprias (textos completos em `NOTICE.md`):

| Modelo | Licença | Uso comercial |
| --- | --- | --- |
| Stable Audio Open 1.0 | Stability AI Community | Até US$1M de receita anual: sim; acima: licença Enterprise |
| opus-mt-mul-en (light) | Apache 2.0 | Sim |
| NLLB-200-distilled-600M (heavy) | CC-BY-NC 4.0 | **Não, apenas não comercial** |

Para uso comercial, escolha o tradutor **light** na instalação.

## Testado em

- Windows 11 Pro
- Python 3.11.9
- NVIDIA RTX 5080 (16 GB VRAM)
- CUDA 12.8
- PyTorch 2.11.0+cu128

## Créditos

- **Stable Audio Open 1.0** — Stability AI
- **opus-mt-mul-en** — Helsinki-NLP / Tatoeba Translation Challenge
- **NLLB-200** — Meta AI / FAIR
- **Gradio**, **diffusers**, **transformers**, **accelerate** — HuggingFace
- **Desenvolvimento do wrapper** — Oscar Lumiere
- **Assistência** — [Claude Code](https://www.anthropic.com/claude-code) (Anthropic)
