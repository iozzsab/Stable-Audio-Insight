**Langue :**
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

## Démarrage rapide

1. Inscrivez-vous sur https://huggingface.co (passez si vous avez déjà un compte)
2. Ouvrez https://huggingface.co/stabilityai/stable-audio-open-1.0 → cliquez sur **Agree and access repository**
3. Sur https://huggingface.co/settings/tokens → **New token** → Type: Read → Create
4. Lancez `install.bat` → choisissez la langue → collez le jeton → choisissez le traducteur. Terminé.

Ensuite `run.bat` ouvre http://127.0.0.1:7860.


Application Windows autonome pour [Stable Audio Open 1.0](https://huggingface.co/stabilityai/stable-audio-open-1.0) de Stability AI. Conçue pour le sound design, l'audio de jeu, le montage vidéo et les esquisses musicales.

## Ce qui est inclus

- **UI en 9 langues** (English, Русский, 中文, 日本語, Español, Français, Deutsch, Português, 한국어) — le sélecteur dans le pied de page Gradio bascule tout à la volée
- **Prompts multilingues** — saisissez en cyrillique / CJK / arabe / hébreu / grec / thaï / devanagari, traduction automatique en anglais avant la génération. Deux options à l'installation : `opus-mt-mul-en` (light, ~300 Mo) ou `nllb-200-distilled-600M` (heavy, ~2,4 Go)
- **~217 presets dans 15 catégories** — Pas, Impacts, Mouvement, UI, Armes, Ambiance, Véhicules, Nature, Musique, Cinématique, Magie, Sci-Fi, Horreur, Animaux, Foule et voix
- **Génération multi-variations** — 1 à 4 audios par clic (`num_waveforms_per_prompt`), sélecteur de scheduler (Default / DPM++ 2M / Euler), bouton seed aléatoire, bouton Re-roll
- **Historique de session** — 10 dernières générations sous forme de mini-lecteurs pliables
- **Mode batch** — collez plusieurs prompts (un par ligne), chacun sauvegardé dans `outputs/Saved/`
- **Export ZIP** de `outputs/Saved/` en un clic
- **Sortie game-ready** — noms de fichiers slug (`wood_floor_footsteps_01.wav`) avec compteur par dossier ; métadonnées WAV INFO avec prompt complet, seed, durée, steps, cfg, fréquence, negative — lues par Reaper, Audition, Ableton, ffprobe
- **Bascule GPU/CPU en direct** et `RunOnCPU.bat` pour systèmes à faible VRAM
- **Journal par session** dans `logs/app-YYYYMMDD-HHMMSS.log` avec traces complètes sur erreur
- **Installeur d'un seul fichier** (`install.bat`) — installe Python 3.11.9 silencieusement dans le dossier du projet, choisit `torch+cu128` ou CPU torch selon `nvidia-smi`, télécharge le modèle et le traducteur. Véritablement portable : supprimer le dossier ne laisse aucune trace
- **Mise à jour** — `update.bat` rafraîchit les dépendances et resynchronise les modèles

## Prérequis

- Windows 10 / 11 (testé sur Windows 11 Pro)
- Python **3.11.x** — https://www.python.org/downloads/release/python-3119/
  (lors de l'installation, cochez **Add Python to PATH**)
- GPU NVIDIA avec CUDA 12.x :
  - **Minimum** : ~4 Go VRAM (fp16, 1 variation, ≤ 20 s, ≤ 100 étapes)
  - **Recommandé** : 8 Go+ VRAM pour 4 variations × 47 s à 100+ étapes
  - 6 Go conviennent à 1–2 variations ; 4 en parallèle peuvent OOM
  - Pour d'autres versions de CUDA, modifiez l'index PyTorch dans
    `install.bat` / `setup.bat` (par exemple `cu121` pour CUDA 12.1)
  - Pas de NVIDIA → utilisez `RunOnCPU.bat` ou le commutateur **GPU/CPU**
    de l'interface (plus lent, mais fonctionne)
- **15–20 Go d'espace libre pendant l'installation** (après : ~10–13 Go résidents) :
  - ~5 Go — poids de Stable Audio Open
  - ~4–5 Go — Python + PyTorch CUDA + dépendances
  - 0,3–2,4 Go — traducteur (au choix)
  - ~5 Go — caches HuggingFace et pip + fichiers temporaires d'installation (la plupart libérables ensuite)
- Compte HuggingFace + jeton de lecture (uniquement pour le téléchargement
  initial)

## Faut-il un jeton HuggingFace ?

**Une seule fois — uniquement pour télécharger les poids de Stable Audio.**
Ensuite l'application fonctionne hors ligne depuis le cache local
`hf-cache/`.

Stable Audio Open 1.0 est un modèle *gated* — Stability AI exige un compte
enregistré et l'acceptation de la licence avant le téléchargement. Donc :

1. Inscrivez-vous sur https://huggingface.co (si ce n'est pas déjà fait)
2. Ouvrez la page du modèle et **acceptez la licence** :
   https://huggingface.co/stabilityai/stable-audio-open-1.0
   (cliquez sur **Agree and access repository** — sans cela, le
   téléchargement renvoie 403)
3. Créez un jeton de lecture : https://huggingface.co/settings/tokens
4. `install.bat` vous demandera de coller le jeton au bon moment

Les traducteurs (`opus-mt-mul-en` et `nllb-200-distilled-600M`) **ne**
demandent **pas** de jeton — ce sont des modèles publics.

## Installation (recommandée)

Un seul fichier fait tout :

```
install.bat
```

Étapes :

1. Choix de la langue des prompts (1–9 : anglais, russe, chinois, japonais,
   espagnol, français, allemand, portugais, coréen)
2. Vérifie que Python 3.11 est dans PATH (`py -3.11`)
3. Crée `.venv` et met à jour pip / wheel
4. Installe PyTorch (CUDA 12.8) et le reste de `requirements.txt`
5. Demande le jeton HF (ou passe si déjà connecté)
6. **Demande quel traducteur installer :**
   - **1. LIGHT** — `Helsinki-NLP/opus-mt-mul-en`
     - ~300 Mo, rapide, Apache 2.0 (commercial OK)
     - Qualité moyenne, parfois faux sur les termes musicaux
   - **2. HEAVY** — `facebook/nllb-200-distilled-600M`
     - ~2,4 Go, plus lent, CC-BY-NC 4.0 (**non commercial uniquement**)
     - Meilleure qualité, recommandé pour le non-anglais
7. Enregistre le choix dans `hf-cache/translator.cfg`
8. Télécharge Stable Audio (~5 Go) et le traducteur choisi dans `hf-cache/`

## Exécution

```
run.bat
```

Un onglet s'ouvre sur http://127.0.0.1:7860.

## Changer de traducteur après installation

Le plus simple :

1. Ouvrez `hf-cache/translator.cfg` et passez à `light` ou `heavy`
2. Lancez `download.bat` — il télécharge le choisi s'il manque
3. `run.bat`

Ou supprimez `hf-cache/translator.cfg` puis relancez `install.bat` — il redemande,
sans retélécharger les dépendances ni Stable Audio (déjà en cache).

## Installation pas à pas (si problème)

`install.bat` enchaîne quatre petits scripts ; chacun peut être lancé
séparément :

| Script | Rôle |
| --- | --- |
| `setup.bat` | Crée `.venv` et installe les dépendances |
| `login.bat` | Authentification HuggingFace (`hf auth login`) |
| `download.bat` | Télécharge Stable Audio + traducteur via `hf-cache/translator.cfg` |
| `run.bat` | Lance l'UI web Gradio |

## Structure du projet

```
.
├── app.py              # UI Gradio + génération
├── translator.py       # Module de traduction (light / heavy)
├── download_model.py   # Téléchargements depuis HuggingFace
├── requirements.txt    # Dépendances Python
├── install.bat         # Installeur unique (multilingue)
├── setup.bat           # Uniquement venv + dépendances
├── login.bat           # Uniquement auth HF
├── download.bat        # Uniquement téléchargements
├── run.bat             # Lance l'UI web
├── hf-cache/translator.cfg  # light / heavy (créé par install.bat)
├── README.md           # main docs (English)
├── docs/i18n/          # localized versions (8 languages)
├── LICENSE             # MIT — pour le code de ce dépôt
├── NOTICE.md           # Licences des modèles utilisés
├── hf-cache/           # Cache HF local (PAS dans git)
└── outputs/            # Audio enregistré (PAS dans git)
    ├── intermediate/   # Quand "Save all" est coché
    └── Saved/          # Quand on clique sur "Save"
```

## Variables d'environnement

Modifiables avant `run.bat` :

| Variable | Défaut | Rôle |
| --- | --- | --- |
| `HOST` | `127.0.0.1` | Hôte Gradio |
| `PORT` | `7860` | Port Gradio |
| `SHARE` | `0` | `1` = créer un lien public gradio.live |
| `STABLE_AUDIO_MODEL` | `stabilityai/stable-audio-open-1.0` | Changer de modèle |

## Licences

Ce **code source** est sous MIT (voir `LICENSE`).

Les **modèles** ont chacun leur licence (texte complet dans `NOTICE.md`) :

| Modèle | Licence | Usage commercial |
| --- | --- | --- |
| Stable Audio Open 1.0 | Stability AI Community | Jusqu'à 1M$ de revenu annuel : oui ; au-delà : licence Enterprise |
| opus-mt-mul-en (light) | Apache 2.0 | Oui |
| NLLB-200-distilled-600M (heavy) | CC-BY-NC 4.0 | **Non, non commercial uniquement** |

Pour un usage commercial, choisissez le traducteur **light** à l'installation.

## Testé sur

- Windows 11 Pro
- Python 3.11.9
- NVIDIA RTX 5080 (16 Go VRAM)
- CUDA 12.8
- PyTorch 2.11.0+cu128

## Crédits

- **Stable Audio Open 1.0** — Stability AI
- **opus-mt-mul-en** — Helsinki-NLP / Tatoeba Translation Challenge
- **NLLB-200** — Meta AI / FAIR
- **Gradio**, **diffusers**, **transformers**, **accelerate** — HuggingFace
- **Développement du wrapper** — Oscar Lumiere
- **Assistance** — [Claude Code](https://www.anthropic.com/claude-code) (Anthropic)
