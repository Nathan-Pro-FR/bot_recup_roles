@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM SCRIPT DE LANCEMENT - Gestionnaire de Rôles Discord (Windows)
REM ═══════════════════════════════════════════════════════════════════════════

echo.
echo ╔═════════════════════════════════════════════════════════════════════════╗
echo ║     BOT DISCORD - GESTIONNAIRE DE RÔLES                                 ║
echo ║     Démarrage en cours...                                              ║
echo ╚═════════════════════════════════════════════════════════════════════════╝
echo.

REM Vérifier si l'environnement virtuel existe
REM Déterminer le chemin du script et la racine du projet
set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%.." >nul 2>&1
if errorlevel 1 (
    echo ❌ Impossible de déterminer la racine du projet.
    pause
    exit /b 1
)
set "PROJECT_ROOT=%CD%"
popd >nul 2>&1

REM Utiliser le venv local dans le dossier scripts si présent, sinon créer dans scripts
set "VENV_DIR=%~dp0venv"
if not exist "%VENV_DIR%" (
    echo ⚠️  Environnement virtuel non trouvé dans %~dp0.
    echo 📦 Création de l'environnement virtuel dans %~dp0venv ...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo ❌ Échec de la création de l'environnement virtuel.
        pause
        exit /b 1
    )
    echo ✅ Environnement virtuel créé.
    echo.
)

REM Activer l'environnement virtuel
call "%VENV_DIR%\Scripts\activate.bat"

REM Vérifier si les dépendances sont installées
echo 📋 Vérification des dépendances...
pip show discord.py >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Dépendances manquantes.
    echo 📥 Installation des dépendances...
    pip install -r "%PROJECT_ROOT%\config\requirements.txt"
    echo ✅ Dépendances installées.
    echo.
)

REM Vérifier le fichier .env dans la racine du projet
if not exist "%PROJECT_ROOT%\config\.env" (
    echo.
    echo ❌ ERREUR: Fichier .env non trouvé!
    echo.
    echo 📝 Étapes pour corriger:
    echo    1. Dupliquez config/.env.example en config/.env
    echo    2. Collez votre TOKEN Discord dans config/.env
    echo    3. Relancez ce script
    echo.
    pause
    exit /b 1
)

echo ✅ Configuration OK
echo.
echo 🚀 Démarrage du bot...
echo.

REM Lancer le bot depuis la racine du projet
python "%PROJECT_ROOT%\bot\bot.py"

REM Pause pour voir les messages d'erreur
pause