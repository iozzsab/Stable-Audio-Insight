@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
chcp 65001 >nul

echo ============================================================
echo   Stable Audio Insight - install
echo ============================================================
echo.
echo Select language / Выберите язык / 选择语言 / 言語を選択
echo Idioma / Langue / Sprache / Idioma / 언어 선택
echo.
echo   1. English
echo   2. Русский (Russian)
echo   3. 中文 (Chinese, Simplified)
echo   4. 日本語 (Japanese)
echo   5. Espanol (Spanish)
echo   6. Francais (French)
echo   7. Deutsch (German)
echo   8. Portugues (Portuguese)
echo   9. 한국어 (Korean)
echo.

:lang_input
set /p LANG_CHOICE=Choice [1-9]:
set "LANG="
if "!LANG_CHOICE!"=="1" set "LANG=en"
if "!LANG_CHOICE!"=="2" set "LANG=ru"
if "!LANG_CHOICE!"=="3" set "LANG=zh"
if "!LANG_CHOICE!"=="4" set "LANG=ja"
if "!LANG_CHOICE!"=="5" set "LANG=es"
if "!LANG_CHOICE!"=="6" set "LANG=fr"
if "!LANG_CHOICE!"=="7" set "LANG=de"
if "!LANG_CHOICE!"=="8" set "LANG=pt"
if "!LANG_CHOICE!"=="9" set "LANG=ko"
if not defined LANG (
    echo Invalid choice. Enter 1-9.
    goto lang_input
)
call :L_!LANG!

goto :main


REM ===== language blocks =====

:L_en
set "MSG_STEP1=[1/6] Checking Python 3.11..."
set "MSG_PYTHON_OK=OK: Python 3.11 found."
set "MSG_PYTHON_FAIL=ERROR: Python 3.11 not found."
set "MSG_PYTHON_INSTALL=Install Python 3.11.x from https://www.python.org/downloads/release/python-3119/"
set "MSG_PATH_REMINDER=During install, check 'Add Python to PATH'."
set "MSG_RERUN=Then run install.bat again."
set "MSG_STEP2=[2/6] Virtual environment..."
set "MSG_VENV_CREATING=Creating venv..."
set "MSG_VENV_FAIL=ERROR: failed to create venv."
set "MSG_VENV_EXISTS=venv already exists, skipping."
set "MSG_STEP3=[3/6] Upgrading pip + installing PyTorch (CUDA 12.8)..."
set "MSG_TORCH_FAIL=ERROR: failed to install PyTorch. Check internet."
set "MSG_DEPS=Installing remaining dependencies..."
set "MSG_DEPS_FAIL=ERROR: failed to install dependencies."
set "MSG_STEP4=[4/6]   ACTION REQUIRED — HuggingFace token"
set "MSG_TOKEN_INTRO=To download the model, you need a HuggingFace account (one-time setup):"
set "MSG_TOKEN_STEP1=1. Register at https://huggingface.co  (skip if you already have an account)"
set "MSG_TOKEN_STEP2=2. Accept the license at https://huggingface.co/stabilityai/stable-audio-open-1.0   -> click 'Agree and access repository'"
set "MSG_TOKEN_STEP3=3. Create a read-only token at https://huggingface.co/settings/tokens   -> 'New token' -> Type: Read -> Create"
set "MSG_TOKEN_STEP4=4. Paste the token in the line below and press Enter."
set "MSG_TOKEN_GET= - Get a read token: https://huggingface.co/settings/tokens"
set "MSG_TOKEN_LICENSE= - Accept the license (once): https://huggingface.co/stabilityai/stable-audio-open-1.0"
set "MSG_TOKEN_INPUT=HF token (or empty if already logged in):"
set "MSG_TOKEN_FAIL=ERROR: login failed. Check the token."
set "MSG_STEP5=[5/6] Choose a translator model (for non-English prompts)"
set "MSG_LIGHT2=             ~300 MB, fast, medium quality"
set "MSG_LIGHT3=             License: Apache 2.0 (commercial OK)"
set "MSG_HEAVY2=             ~2.4 GB, high quality, recommended"
set "MSG_HEAVY3=             License: CC-BY-NC 4.0 (NON-COMMERCIAL ONLY)"
set "MSG_TR_INPUT=Enter 1 or 2:"
set "MSG_TR_INVALID=Enter 1 or 2."
set "MSG_TR_SAVED=Saved in translator.cfg:"
set "MSG_STEP6=[6/6] Downloading models (Stable Audio ~5 GB + translator)..."
set "MSG_DL_FAIL=ERROR: failed to download models."
set "MSG_DONE=Installation complete!"
set "MSG_RUN_INFO=Run: run.bat (opens http://127.0.0.1:7860)"
set "MSG_SWITCH1=To change the translator: delete translator.cfg and re-run install.bat,"
set "MSG_SWITCH2=or edit it manually (light/heavy) and run download.bat."
goto :eof

:L_ru
set "MSG_STEP1=[1/6] Проверка Python 3.11..."
set "MSG_PYTHON_OK=OK: Python 3.11 найден."
set "MSG_PYTHON_FAIL=ОШИБКА: Python 3.11 не найден."
set "MSG_PYTHON_INSTALL=Установите Python 3.11.x с https://www.python.org/downloads/release/python-3119/"
set "MSG_PATH_REMINDER=При установке отметьте 'Add Python to PATH'."
set "MSG_RERUN=Затем запустите install.bat снова."
set "MSG_STEP2=[2/6] Виртуальное окружение..."
set "MSG_VENV_CREATING=Создаю venv..."
set "MSG_VENV_FAIL=ОШИБКА: не удалось создать venv."
set "MSG_VENV_EXISTS=venv уже существует, пропускаю."
set "MSG_STEP3=[3/6] Обновление pip + установка PyTorch (CUDA 12.8)..."
set "MSG_TORCH_FAIL=ОШИБКА: не удалось установить PyTorch. Проверьте интернет."
set "MSG_DEPS=Установка остальных зависимостей..."
set "MSG_DEPS_FAIL=ОШИБКА: не удалось установить зависимости."
set "MSG_STEP4=[4/6]   НУЖНО ДЕЙСТВИЕ — токен HuggingFace"
set "MSG_TOKEN_INTRO=Чтобы скачать модель, нужен аккаунт на HuggingFace (одноразовая настройка):"
set "MSG_TOKEN_STEP1=1. Зарегистрируйтесь на https://huggingface.co  (пропустите, если аккаунт уже есть)"
set "MSG_TOKEN_STEP2=2. Примите лицензию на https://huggingface.co/stabilityai/stable-audio-open-1.0   -> кнопка 'Agree and access repository'"
set "MSG_TOKEN_STEP3=3. Создайте read-токен на https://huggingface.co/settings/tokens   -> 'New token' -> Type: Read -> Create"
set "MSG_TOKEN_STEP4=4. Вставьте токен в строку ниже и нажмите Enter."
set "MSG_TOKEN_GET= - Получите read-токен: https://huggingface.co/settings/tokens"
set "MSG_TOKEN_LICENSE= - Примите лицензию (один раз): https://huggingface.co/stabilityai/stable-audio-open-1.0"
set "MSG_TOKEN_INPUT=HF токен (или пусто, если уже залогинились):"
set "MSG_TOKEN_FAIL=ОШИБКА: не удалось залогиниться. Проверьте токен."
set "MSG_STEP5=[5/6] Выберите модель-переводчик (для не-английских промптов)"
set "MSG_LIGHT2=             ~300 МБ, быстрая, среднее качество"
set "MSG_LIGHT3=             Лицензия: Apache 2.0 (можно коммерчески)"
set "MSG_HEAVY2=             ~2.4 ГБ, высокое качество, рекомендуется"
set "MSG_HEAVY3=             Лицензия: CC-BY-NC 4.0 (ТОЛЬКО НЕКОММЕРЧЕСКОЕ)"
set "MSG_TR_INPUT=Введите 1 или 2:"
set "MSG_TR_INVALID=Введите 1 или 2."
set "MSG_TR_SAVED=Сохранено в translator.cfg:"
set "MSG_STEP6=[6/6] Скачивание моделей (Stable Audio ~5 ГБ + переводчик)..."
set "MSG_DL_FAIL=ОШИБКА: не удалось скачать модели."
set "MSG_DONE=Установка завершена!"
set "MSG_RUN_INFO=Запуск: run.bat (откроет http://127.0.0.1:7860)"
set "MSG_SWITCH1=Сменить переводчик: удалите translator.cfg и запустите install.bat снова,"
set "MSG_SWITCH2=или измените его вручную (light/heavy) и запустите download.bat."
goto :eof

:L_zh
set "MSG_STEP1=[1/6] 检查 Python 3.11..."
set "MSG_PYTHON_OK=已找到 Python 3.11."
set "MSG_PYTHON_FAIL=错误：未找到 Python 3.11。"
set "MSG_PYTHON_INSTALL=请从 https://www.python.org/downloads/release/python-3119/ 安装 Python 3.11.x"
set "MSG_PATH_REMINDER=安装时请勾选 'Add Python to PATH'。"
set "MSG_RERUN=然后再次运行 install.bat。"
set "MSG_STEP2=[2/6] 虚拟环境..."
set "MSG_VENV_CREATING=正在创建 venv..."
set "MSG_VENV_FAIL=错误：无法创建 venv。"
set "MSG_VENV_EXISTS=venv 已存在，跳过。"
set "MSG_STEP3=[3/6] 升级 pip + 安装 PyTorch (CUDA 12.8)..."
set "MSG_TORCH_FAIL=错误：无法安装 PyTorch。请检查网络连接。"
set "MSG_DEPS=正在安装其他依赖..."
set "MSG_DEPS_FAIL=错误：依赖安装失败。"
set "MSG_STEP4=[4/6]   需要操作 — HuggingFace 令牌"
set "MSG_TOKEN_INTRO=要下载模型，需要 HuggingFace 账号（一次性设置）："
set "MSG_TOKEN_STEP1=1. 在 https://huggingface.co 注册（如已注册请跳过）"
set "MSG_TOKEN_STEP2=2. 接受模型许可：https://huggingface.co/stabilityai/stable-audio-open-1.0  -> 点击 'Agree and access repository'"
set "MSG_TOKEN_STEP3=3. 创建 read 令牌：https://huggingface.co/settings/tokens  -> 'New token' -> Type: Read -> Create"
set "MSG_TOKEN_STEP4=4. 把令牌粘贴到下面并按 Enter。"
set "MSG_TOKEN_GET= - 获取 read 令牌：https://huggingface.co/settings/tokens"
set "MSG_TOKEN_LICENSE= - 接受模型许可（一次）：https://huggingface.co/stabilityai/stable-audio-open-1.0"
set "MSG_TOKEN_INPUT=HF 令牌（如已登录可留空）："
set "MSG_TOKEN_FAIL=错误：登录失败。请检查令牌。"
set "MSG_STEP5=[5/6] 选择翻译模型（用于非英语提示）"
set "MSG_LIGHT2=             ~300 MB，快速，中等质量"
set "MSG_LIGHT3=             许可：Apache 2.0（允许商用）"
set "MSG_HEAVY2=             ~2.4 GB，高质量，推荐"
set "MSG_HEAVY3=             许可：CC-BY-NC 4.0（仅限非商业用途）"
set "MSG_TR_INPUT=输入 1 或 2："
set "MSG_TR_INVALID=请输入 1 或 2。"
set "MSG_TR_SAVED=已保存到 translator.cfg："
set "MSG_STEP6=[6/6] 下载模型（Stable Audio ~5 GB + 翻译器）..."
set "MSG_DL_FAIL=错误：模型下载失败。"
set "MSG_DONE=安装完成！"
set "MSG_RUN_INFO=运行：run.bat（打开 http://127.0.0.1:7860）"
set "MSG_SWITCH1=更换翻译器：删除 translator.cfg 并再次运行 install.bat，"
set "MSG_SWITCH2=或手动编辑（light/heavy）后运行 download.bat。"
goto :eof

:L_ja
set "MSG_STEP1=[1/6] Python 3.11 を確認しています..."
set "MSG_PYTHON_OK=Python 3.11 が見つかりました。"
set "MSG_PYTHON_FAIL=エラー: Python 3.11 が見つかりません。"
set "MSG_PYTHON_INSTALL=https://www.python.org/downloads/release/python-3119/ から Python 3.11.x をインストールしてください"
set "MSG_PATH_REMINDER=インストール時に 'Add Python to PATH' をチェックしてください。"
set "MSG_RERUN=その後 install.bat を再度実行してください。"
set "MSG_STEP2=[2/6] 仮想環境..."
set "MSG_VENV_CREATING=venv を作成しています..."
set "MSG_VENV_FAIL=エラー: venv の作成に失敗しました。"
set "MSG_VENV_EXISTS=venv は既に存在します、スキップします。"
set "MSG_STEP3=[3/6] pip をアップグレードし PyTorch (CUDA 12.8) をインストール中..."
set "MSG_TORCH_FAIL=エラー: PyTorch のインストールに失敗しました。ネット接続を確認してください。"
set "MSG_DEPS=残りの依存関係をインストール中..."
set "MSG_DEPS_FAIL=エラー: 依存関係のインストールに失敗しました。"
set "MSG_STEP4=[4/6]   操作が必要 — HuggingFace トークン"
set "MSG_TOKEN_INTRO=モデルをダウンロードするには HuggingFace アカウントが必要です（初回のみ）:"
set "MSG_TOKEN_STEP1=1. https://huggingface.co で登録（既にあればスキップ）"
set "MSG_TOKEN_STEP2=2. ライセンスに同意: https://huggingface.co/stabilityai/stable-audio-open-1.0  -> 'Agree and access repository' をクリック"
set "MSG_TOKEN_STEP3=3. read トークン作成: https://huggingface.co/settings/tokens  -> 'New token' -> Type: Read -> Create"
set "MSG_TOKEN_STEP4=4. 下の入力欄にトークンを貼り付けて Enter。"
set "MSG_TOKEN_GET= - read トークンを取得: https://huggingface.co/settings/tokens"
set "MSG_TOKEN_LICENSE= - ライセンスに同意（1回）: https://huggingface.co/stabilityai/stable-audio-open-1.0"
set "MSG_TOKEN_INPUT=HF トークン (ログイン済みなら空のままで):"
set "MSG_TOKEN_FAIL=エラー: ログインに失敗しました。トークンを確認してください。"
set "MSG_STEP5=[5/6] 翻訳モデルを選択 (英語以外のプロンプト用)"
set "MSG_LIGHT2=             約300 MB、高速、品質は中程度"
set "MSG_LIGHT3=             ライセンス: Apache 2.0 (商用OK)"
set "MSG_HEAVY2=             約2.4 GB、高品質、推奨"
set "MSG_HEAVY3=             ライセンス: CC-BY-NC 4.0 (非商用のみ)"
set "MSG_TR_INPUT=1 または 2 を入力:"
set "MSG_TR_INVALID=1 または 2 を入力してください。"
set "MSG_TR_SAVED=translator.cfg に保存しました:"
set "MSG_STEP6=[6/6] モデルをダウンロード中 (Stable Audio ~5 GB + 翻訳モデル)..."
set "MSG_DL_FAIL=エラー: モデルのダウンロードに失敗しました。"
set "MSG_DONE=インストール完了！"
set "MSG_RUN_INFO=実行: run.bat (http://127.0.0.1:7860 を開きます)"
set "MSG_SWITCH1=翻訳モデルを変更: translator.cfg を削除し install.bat を再実行、"
set "MSG_SWITCH2=または手動で編集 (light/heavy) し download.bat を実行。"
goto :eof

:L_es
set "MSG_STEP1=[1/6] Comprobando Python 3.11..."
set "MSG_PYTHON_OK=OK: Python 3.11 encontrado."
set "MSG_PYTHON_FAIL=ERROR: Python 3.11 no encontrado."
set "MSG_PYTHON_INSTALL=Instale Python 3.11.x desde https://www.python.org/downloads/release/python-3119/"
set "MSG_PATH_REMINDER=Durante la instalacion marque 'Add Python to PATH'."
set "MSG_RERUN=Luego ejecute install.bat de nuevo."
set "MSG_STEP2=[2/6] Entorno virtual..."
set "MSG_VENV_CREATING=Creando venv..."
set "MSG_VENV_FAIL=ERROR: no se pudo crear venv."
set "MSG_VENV_EXISTS=venv ya existe, omitiendo."
set "MSG_STEP3=[3/6] Actualizando pip + instalando PyTorch (CUDA 12.8)..."
set "MSG_TORCH_FAIL=ERROR: no se pudo instalar PyTorch. Compruebe su conexion."
set "MSG_DEPS=Instalando dependencias restantes..."
set "MSG_DEPS_FAIL=ERROR: no se pudieron instalar las dependencias."
set "MSG_STEP4=[4/6]   ACCION REQUERIDA — token HuggingFace"
set "MSG_TOKEN_INTRO=Para descargar el modelo necesita una cuenta HuggingFace (configuracion unica):"
set "MSG_TOKEN_STEP1=1. Registrese en https://huggingface.co  (omitir si ya tiene cuenta)"
set "MSG_TOKEN_STEP2=2. Acepte la licencia: https://huggingface.co/stabilityai/stable-audio-open-1.0  -> haga clic en 'Agree and access repository'"
set "MSG_TOKEN_STEP3=3. Cree un token de lectura: https://huggingface.co/settings/tokens  -> 'New token' -> Type: Read -> Create"
set "MSG_TOKEN_STEP4=4. Pegue el token abajo y pulse Enter."
set "MSG_TOKEN_GET= - Obtenga un token (read): https://huggingface.co/settings/tokens"
set "MSG_TOKEN_LICENSE= - Acepte la licencia (una vez): https://huggingface.co/stabilityai/stable-audio-open-1.0"
set "MSG_TOKEN_INPUT=Token HF (o vacio si ya inicio sesion):"
set "MSG_TOKEN_FAIL=ERROR: fallo el inicio de sesion. Verifique el token."
set "MSG_STEP5=[5/6] Elija el modelo de traduccion (para prompts no en ingles)"
set "MSG_LIGHT2=             ~300 MB, rapido, calidad media"
set "MSG_LIGHT3=             Licencia: Apache 2.0 (uso comercial permitido)"
set "MSG_HEAVY2=             ~2.4 GB, alta calidad, recomendado"
set "MSG_HEAVY3=             Licencia: CC-BY-NC 4.0 (SOLO USO NO COMERCIAL)"
set "MSG_TR_INPUT=Introduzca 1 o 2:"
set "MSG_TR_INVALID=Introduzca 1 o 2."
set "MSG_TR_SAVED=Guardado en translator.cfg:"
set "MSG_STEP6=[6/6] Descargando modelos (Stable Audio ~5 GB + traductor)..."
set "MSG_DL_FAIL=ERROR: no se pudieron descargar los modelos."
set "MSG_DONE=Instalacion completa!"
set "MSG_RUN_INFO=Ejecutar: run.bat (abre http://127.0.0.1:7860)"
set "MSG_SWITCH1=Cambiar traductor: elimine translator.cfg y ejecute install.bat de nuevo,"
set "MSG_SWITCH2=o editelo manualmente (light/heavy) y ejecute download.bat."
goto :eof

:L_fr
set "MSG_STEP1=[1/6] Verification de Python 3.11..."
set "MSG_PYTHON_OK=OK: Python 3.11 trouve."
set "MSG_PYTHON_FAIL=ERREUR: Python 3.11 introuvable."
set "MSG_PYTHON_INSTALL=Installez Python 3.11.x depuis https://www.python.org/downloads/release/python-3119/"
set "MSG_PATH_REMINDER=Pendant l'installation, cochez 'Add Python to PATH'."
set "MSG_RERUN=Puis relancez install.bat."
set "MSG_STEP2=[2/6] Environnement virtuel..."
set "MSG_VENV_CREATING=Creation du venv..."
set "MSG_VENV_FAIL=ERREUR: echec de la creation du venv."
set "MSG_VENV_EXISTS=venv existe deja, ignore."
set "MSG_STEP3=[3/6] Mise a jour de pip + installation de PyTorch (CUDA 12.8)..."
set "MSG_TORCH_FAIL=ERREUR: echec de l'installation de PyTorch. Verifiez votre connexion."
set "MSG_DEPS=Installation des dependances restantes..."
set "MSG_DEPS_FAIL=ERREUR: echec de l'installation des dependances."
set "MSG_STEP4=[4/6]   ACTION REQUISE — jeton HuggingFace"
set "MSG_TOKEN_INTRO=Pour telecharger le modele il faut un compte HuggingFace (configuration unique):"
set "MSG_TOKEN_STEP1=1. Inscrivez-vous sur https://huggingface.co  (passez si vous avez deja un compte)"
set "MSG_TOKEN_STEP2=2. Acceptez la licence: https://huggingface.co/stabilityai/stable-audio-open-1.0  -> cliquez sur 'Agree and access repository'"
set "MSG_TOKEN_STEP3=3. Creez un jeton read: https://huggingface.co/settings/tokens  -> 'New token' -> Type: Read -> Create"
set "MSG_TOKEN_STEP4=4. Collez le jeton ci-dessous et appuyez sur Entree."
set "MSG_TOKEN_GET= - Obtenez un jeton (read): https://huggingface.co/settings/tokens"
set "MSG_TOKEN_LICENSE= - Acceptez la licence (une fois): https://huggingface.co/stabilityai/stable-audio-open-1.0"
set "MSG_TOKEN_INPUT=Jeton HF (vide si deja connecte):"
set "MSG_TOKEN_FAIL=ERREUR: echec de la connexion. Verifiez le jeton."
set "MSG_STEP5=[5/6] Choisissez le modele de traduction (pour prompts non anglais)"
set "MSG_LIGHT2=             ~300 Mo, rapide, qualite moyenne"
set "MSG_LIGHT3=             Licence: Apache 2.0 (commercial OK)"
set "MSG_HEAVY2=             ~2,4 Go, haute qualite, recommande"
set "MSG_HEAVY3=             Licence: CC-BY-NC 4.0 (NON COMMERCIAL UNIQUEMENT)"
set "MSG_TR_INPUT=Entrez 1 ou 2:"
set "MSG_TR_INVALID=Entrez 1 ou 2."
set "MSG_TR_SAVED=Enregistre dans translator.cfg:"
set "MSG_STEP6=[6/6] Telechargement des modeles (Stable Audio ~5 Go + traducteur)..."
set "MSG_DL_FAIL=ERREUR: echec du telechargement des modeles."
set "MSG_DONE=Installation terminee !"
set "MSG_RUN_INFO=Lancer: run.bat (ouvre http://127.0.0.1:7860)"
set "MSG_SWITCH1=Changer le traducteur: supprimez translator.cfg et relancez install.bat,"
set "MSG_SWITCH2=ou modifiez-le manuellement (light/heavy) et lancez download.bat."
goto :eof

:L_de
set "MSG_STEP1=[1/6] Pruefe Python 3.11..."
set "MSG_PYTHON_OK=OK: Python 3.11 gefunden."
set "MSG_PYTHON_FAIL=FEHLER: Python 3.11 nicht gefunden."
set "MSG_PYTHON_INSTALL=Installieren Sie Python 3.11.x von https://www.python.org/downloads/release/python-3119/"
set "MSG_PATH_REMINDER=Wahlen Sie bei der Installation 'Add Python to PATH' aus."
set "MSG_RERUN=Fuhren Sie dann install.bat erneut aus."
set "MSG_STEP2=[2/6] Virtuelle Umgebung..."
set "MSG_VENV_CREATING=Erstelle venv..."
set "MSG_VENV_FAIL=FEHLER: venv konnte nicht erstellt werden."
set "MSG_VENV_EXISTS=venv existiert bereits, uberspringe."
set "MSG_STEP3=[3/6] pip aktualisieren + PyTorch (CUDA 12.8) installieren..."
set "MSG_TORCH_FAIL=FEHLER: PyTorch-Installation fehlgeschlagen. Internet pruefen."
set "MSG_DEPS=Installiere weitere Abhangigkeiten..."
set "MSG_DEPS_FAIL=FEHLER: Abhangigkeiten konnten nicht installiert werden."
set "MSG_STEP4=[4/6]   AKTION ERFORDERLICH — HuggingFace-Token"
set "MSG_TOKEN_INTRO=Zum Herunterladen des Modells brauchen Sie ein HuggingFace-Konto (einmalig):"
set "MSG_TOKEN_STEP1=1. Registrieren auf https://huggingface.co  (uberspringen, wenn Sie schon ein Konto haben)"
set "MSG_TOKEN_STEP2=2. Lizenz akzeptieren: https://huggingface.co/stabilityai/stable-audio-open-1.0  -> 'Agree and access repository' klicken"
set "MSG_TOKEN_STEP3=3. read-Token erstellen: https://huggingface.co/settings/tokens  -> 'New token' -> Type: Read -> Create"
set "MSG_TOKEN_STEP4=4. Token unten einfuegen und Enter druecken."
set "MSG_TOKEN_GET= - read-Token holen: https://huggingface.co/settings/tokens"
set "MSG_TOKEN_LICENSE= - Lizenz akzeptieren (einmalig): https://huggingface.co/stabilityai/stable-audio-open-1.0"
set "MSG_TOKEN_INPUT=HF-Token (leer lassen, falls bereits angemeldet):"
set "MSG_TOKEN_FAIL=FEHLER: Anmeldung fehlgeschlagen. Token pruefen."
set "MSG_STEP5=[5/6] Ubersetzermodell wahlen (fuer nicht-englische Prompts)"
set "MSG_LIGHT2=             ~300 MB, schnell, mittlere Qualitat"
set "MSG_LIGHT3=             Lizenz: Apache 2.0 (kommerziell erlaubt)"
set "MSG_HEAVY2=             ~2,4 GB, hohe Qualitat, empfohlen"
set "MSG_HEAVY3=             Lizenz: CC-BY-NC 4.0 (NUR NICHT-KOMMERZIELL)"
set "MSG_TR_INPUT=Geben Sie 1 oder 2 ein:"
set "MSG_TR_INVALID=Geben Sie 1 oder 2 ein."
set "MSG_TR_SAVED=In translator.cfg gespeichert:"
set "MSG_STEP6=[6/6] Lade Modelle herunter (Stable Audio ~5 GB + Ubersetzer)..."
set "MSG_DL_FAIL=FEHLER: Modelle konnten nicht heruntergeladen werden."
set "MSG_DONE=Installation abgeschlossen!"
set "MSG_RUN_INFO=Starten: run.bat (oeffnet http://127.0.0.1:7860)"
set "MSG_SWITCH1=Ubersetzer wechseln: translator.cfg loschen und install.bat erneut ausfuhren,"
set "MSG_SWITCH2=oder manuell bearbeiten (light/heavy) und download.bat ausfuhren."
goto :eof

:L_pt
set "MSG_STEP1=[1/6] Verificando Python 3.11..."
set "MSG_PYTHON_OK=OK: Python 3.11 encontrado."
set "MSG_PYTHON_FAIL=ERRO: Python 3.11 nao encontrado."
set "MSG_PYTHON_INSTALL=Instale Python 3.11.x em https://www.python.org/downloads/release/python-3119/"
set "MSG_PATH_REMINDER=Durante a instalacao, marque 'Add Python to PATH'."
set "MSG_RERUN=Em seguida, execute install.bat novamente."
set "MSG_STEP2=[2/6] Ambiente virtual..."
set "MSG_VENV_CREATING=Criando venv..."
set "MSG_VENV_FAIL=ERRO: falha ao criar venv."
set "MSG_VENV_EXISTS=venv ja existe, ignorando."
set "MSG_STEP3=[3/6] Atualizando pip + instalando PyTorch (CUDA 12.8)..."
set "MSG_TORCH_FAIL=ERRO: falha ao instalar PyTorch. Verifique a internet."
set "MSG_DEPS=Instalando dependencias restantes..."
set "MSG_DEPS_FAIL=ERRO: falha ao instalar dependencias."
set "MSG_STEP4=[4/6]   ACAO NECESSARIA — token HuggingFace"
set "MSG_TOKEN_INTRO=Para baixar o modelo voce precisa de uma conta HuggingFace (uma unica vez):"
set "MSG_TOKEN_STEP1=1. Cadastre-se em https://huggingface.co  (pule se ja tiver conta)"
set "MSG_TOKEN_STEP2=2. Aceite a licenca: https://huggingface.co/stabilityai/stable-audio-open-1.0  -> clique em 'Agree and access repository'"
set "MSG_TOKEN_STEP3=3. Crie um token de leitura: https://huggingface.co/settings/tokens  -> 'New token' -> Type: Read -> Create"
set "MSG_TOKEN_STEP4=4. Cole o token abaixo e pressione Enter."
set "MSG_TOKEN_GET= - Obtenha um token (read): https://huggingface.co/settings/tokens"
set "MSG_TOKEN_LICENSE= - Aceite a licenca (uma vez): https://huggingface.co/stabilityai/stable-audio-open-1.0"
set "MSG_TOKEN_INPUT=Token HF (vazio se ja logado):"
set "MSG_TOKEN_FAIL=ERRO: falha no login. Verifique o token."
set "MSG_STEP5=[5/6] Escolha o modelo de traducao (para prompts nao em ingles)"
set "MSG_LIGHT2=             ~300 MB, rapido, qualidade media"
set "MSG_LIGHT3=             Licenca: Apache 2.0 (uso comercial OK)"
set "MSG_HEAVY2=             ~2.4 GB, alta qualidade, recomendado"
set "MSG_HEAVY3=             Licenca: CC-BY-NC 4.0 (APENAS NAO COMERCIAL)"
set "MSG_TR_INPUT=Digite 1 ou 2:"
set "MSG_TR_INVALID=Digite 1 ou 2."
set "MSG_TR_SAVED=Salvo em translator.cfg:"
set "MSG_STEP6=[6/6] Baixando modelos (Stable Audio ~5 GB + tradutor)..."
set "MSG_DL_FAIL=ERRO: falha no download dos modelos."
set "MSG_DONE=Instalacao concluida!"
set "MSG_RUN_INFO=Executar: run.bat (abre http://127.0.0.1:7860)"
set "MSG_SWITCH1=Trocar tradutor: exclua translator.cfg e execute install.bat novamente,"
set "MSG_SWITCH2=ou edite manualmente (light/heavy) e execute download.bat."
goto :eof

:L_ko
set "MSG_STEP1=[1/6] Python 3.11 확인 중..."
set "MSG_PYTHON_OK=Python 3.11 발견됨."
set "MSG_PYTHON_FAIL=오류: Python 3.11 을 찾을 수 없습니다."
set "MSG_PYTHON_INSTALL=https://www.python.org/downloads/release/python-3119/ 에서 Python 3.11.x 를 설치하세요"
set "MSG_PATH_REMINDER=설치 시 'Add Python to PATH' 옵션을 선택하세요."
set "MSG_RERUN=그런 다음 install.bat 을 다시 실행하세요."
set "MSG_STEP2=[2/6] 가상 환경..."
set "MSG_VENV_CREATING=venv 생성 중..."
set "MSG_VENV_FAIL=오류: venv 생성에 실패했습니다."
set "MSG_VENV_EXISTS=venv 가 이미 존재하므로 건너뜁니다."
set "MSG_STEP3=[3/6] pip 업그레이드 및 PyTorch (CUDA 12.8) 설치 중..."
set "MSG_TORCH_FAIL=오류: PyTorch 설치 실패. 인터넷 연결을 확인하세요."
set "MSG_DEPS=나머지 종속성 설치 중..."
set "MSG_DEPS_FAIL=오류: 종속성 설치에 실패했습니다."
set "MSG_STEP4=[4/6]   조치 필요 — HuggingFace 토큰"
set "MSG_TOKEN_INTRO=모델 다운로드를 위해 HuggingFace 계정이 필요합니다 (최초 1회 설정):"
set "MSG_TOKEN_STEP1=1. https://huggingface.co 에서 회원가입  (계정이 있으면 건너뛰기)"
set "MSG_TOKEN_STEP2=2. 라이선스 동의: https://huggingface.co/stabilityai/stable-audio-open-1.0  -> 'Agree and access repository' 클릭"
set "MSG_TOKEN_STEP3=3. read 토큰 발급: https://huggingface.co/settings/tokens  -> 'New token' -> Type: Read -> Create"
set "MSG_TOKEN_STEP4=4. 아래에 토큰을 붙여 넣고 Enter 누르기."
set "MSG_TOKEN_GET= - read 토큰 발급: https://huggingface.co/settings/tokens"
set "MSG_TOKEN_LICENSE= - 라이선스 동의 (1회): https://huggingface.co/stabilityai/stable-audio-open-1.0"
set "MSG_TOKEN_INPUT=HF 토큰 (이미 로그인했다면 비워 두세요):"
set "MSG_TOKEN_FAIL=오류: 로그인 실패. 토큰을 확인하세요."
set "MSG_STEP5=[5/6] 번역 모델 선택 (영어가 아닌 프롬프트용)"
set "MSG_LIGHT2=             ~300 MB, 빠름, 보통 품질"
set "MSG_LIGHT3=             라이선스: Apache 2.0 (상업적 사용 가능)"
set "MSG_HEAVY2=             ~2.4 GB, 고품질, 권장"
set "MSG_HEAVY3=             라이선스: CC-BY-NC 4.0 (비상업적 사용만 허용)"
set "MSG_TR_INPUT=1 또는 2 입력:"
set "MSG_TR_INVALID=1 또는 2 를 입력하세요."
set "MSG_TR_SAVED=translator.cfg 에 저장됨:"
set "MSG_STEP6=[6/6] 모델 다운로드 중 (Stable Audio ~5 GB + 번역기)..."
set "MSG_DL_FAIL=오류: 모델 다운로드 실패."
set "MSG_DONE=설치 완료!"
set "MSG_RUN_INFO=실행: run.bat (http://127.0.0.1:7860 에서 열림)"
set "MSG_SWITCH1=번역기 변경: translator.cfg 를 삭제하고 install.bat 을 다시 실행,"
set "MSG_SWITCH2=또는 직접 수정 (light/heavy) 후 download.bat 을 실행."
goto :eof


REM ===== main flow =====

:main
set "PORTABLE_DIR=%~dp0python-portable"
set "PY_BIN="
set "HF_BIN="

echo.
echo !MSG_STEP1!

REM 1) Existing portable Python (preferred — fully self-contained in project)
if exist "!PORTABLE_DIR!\python.exe" (
    set "PY_BIN=!PORTABLE_DIR!\python.exe"
    if exist "!PORTABLE_DIR!\Scripts\hf.exe" set "HF_BIN=!PORTABLE_DIR!\Scripts\hf.exe"
    echo Found portable Python: !PY_BIN!
    goto python_ok
)

REM 2) Existing legacy .venv (back-compat with earlier dev setup)
if exist "%~dp0.venv\Scripts\python.exe" (
    "%~dp0.venv\Scripts\python.exe" --version >nul 2>&1
    if not errorlevel 1 (
        set "PY_BIN=%~dp0.venv\Scripts\python.exe"
        if exist "%~dp0.venv\Scripts\hf.exe" set "HF_BIN=%~dp0.venv\Scripts\hf.exe"
        echo Found existing .venv: !PY_BIN!
        goto python_ok
    )
)

REM 3) Auto-install Python 3.11.9 directly into the project folder
echo No Python found in project. Installing Python 3.11.9 to !PORTABLE_DIR! ...
set "PY_INSTALLER=%TEMP%\python-3.11.9-amd64.exe"
if not exist "!PY_INSTALLER!" (
    echo Downloading Python installer ^(~25 MB^)...
    powershell -NoProfile -Command "[Net.ServicePointManager]::SecurityProtocol='Tls12'; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile '%TEMP%\python-3.11.9-amd64.exe'"
    if not exist "!PY_INSTALLER!" (
        echo ERROR: download failed. Check internet connection.
        pause
        exit /b 1
    )
)
echo Running silent install ^(in-project, no PATH changes^)...
"!PY_INSTALLER!" /quiet InstallAllUsers=0 TargetDir="!PORTABLE_DIR!" AssociateFiles=0 Shortcuts=0 PrependPath=0 Include_launcher=0 Include_test=0 Include_doc=0 Include_dev=0 Include_pip=1
if errorlevel 1 (
    echo ERROR: Python installer failed. See %TEMP%\Python*.log for details.
    pause
    exit /b 1
)
del "!PY_INSTALLER!" >nul 2>&1
if not exist "!PORTABLE_DIR!\python.exe" (
    echo ERROR: install completed but python.exe not found at !PORTABLE_DIR!\python.exe
    pause
    exit /b 1
)
set "PY_BIN=!PORTABLE_DIR!\python.exe"

:python_ok
echo !MSG_PYTHON_OK! ^(!PY_BIN!^)

echo.
echo !MSG_STEP3!
"!PY_BIN!" -m pip install --upgrade pip wheel

REM Auto-detect NVIDIA GPU; install matching torch wheels.
nvidia-smi >nul 2>&1
if not errorlevel 1 (
    echo NVIDIA GPU detected — installing torch with CUDA 12.8...
    "!PY_BIN!" -m pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu128
) else (
    echo No NVIDIA GPU detected — installing torch ^(CPU only^)...
    "!PY_BIN!" -m pip install torch torchaudio
)
if errorlevel 1 (
    echo !MSG_TORCH_FAIL!
    pause
    exit /b 1
)
echo.
echo !MSG_DEPS!
"!PY_BIN!" -m pip install -r requirements.txt
if errorlevel 1 (
    echo !MSG_DEPS_FAIL!
    pause
    exit /b 1
)

REM hf.exe lives in the python-portable\Scripts after pip install
if not defined HF_BIN (
    if exist "!PORTABLE_DIR!\Scripts\hf.exe" set "HF_BIN=!PORTABLE_DIR!\Scripts\hf.exe"
    if not defined HF_BIN if exist "%~dp0.venv\Scripts\hf.exe" set "HF_BIN=%~dp0.venv\Scripts\hf.exe"
)

echo.
echo ============================================================
echo   !MSG_STEP4!
echo ============================================================
echo.
echo !MSG_TOKEN_INTRO!
echo.
echo   !MSG_TOKEN_STEP1!
echo.
echo   !MSG_TOKEN_STEP2!
echo.
echo   !MSG_TOKEN_STEP3!
echo.
echo   !MSG_TOKEN_STEP4!
echo.
echo ------------------------------------------------------------
set "HF_HOME=%~dp0hf-cache"
set /p HF_TOKEN_INPUT=!MSG_TOKEN_INPUT!
if not "!HF_TOKEN_INPUT!"=="" (
    if defined HF_BIN (
        "!HF_BIN!" auth login --token !HF_TOKEN_INPUT!
    ) else (
        "!PY_BIN!" -m huggingface_hub.commands.huggingface_cli login --token !HF_TOKEN_INPUT!
    )
    if errorlevel 1 (
        echo !MSG_TOKEN_FAIL!
        pause
        exit /b 1
    )
)

echo.
echo !MSG_STEP5!
echo.
echo   1. LIGHT  - Helsinki-NLP/opus-mt-mul-en
echo !MSG_LIGHT2!
echo !MSG_LIGHT3!
echo.
echo   2. HEAVY  - facebook/nllb-200-distilled-600M
echo !MSG_HEAVY2!
echo !MSG_HEAVY3!
echo.
:choose_translator
set /p TR_CHOICE=!MSG_TR_INPUT!
set "TR_KIND="
if "!TR_CHOICE!"=="1" set "TR_KIND=light"
if "!TR_CHOICE!"=="2" set "TR_KIND=heavy"
if not defined TR_KIND (
    echo !MSG_TR_INVALID!
    goto choose_translator
)
if not exist "%~dp0hf-cache" mkdir "%~dp0hf-cache"
> "%~dp0hf-cache\translator.cfg" echo !TR_KIND!
echo !MSG_TR_SAVED! !TR_KIND!

echo.
echo !MSG_STEP6!
set "PYTHONUNBUFFERED=1"
set "PYTHONIOENCODING=utf-8"
"!PY_BIN!" src\download_model.py
if errorlevel 1 (
    echo.
    echo !MSG_DL_FAIL!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   !MSG_DONE!
echo.
echo   !MSG_RUN_INFO!
echo.
echo   !MSG_SWITCH1!
echo   !MSG_SWITCH2!
echo ============================================================
pause
