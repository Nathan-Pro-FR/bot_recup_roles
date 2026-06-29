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
if not exist "venv" (
    echo ⚠️  Environnement virtuel non trouvé.
    echo 📦 Création de l'environnement virtuel...
    python -m venv venv
    echo ✅ Environnement virtuel créé.
    echo.
)

REM Activer l'environnement virtuel
call venv\Scripts\activate.bat

REM Vérifier si les dépendances sont installées
echo 📋 Vérification des dépendances...
pip show discord.py >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Dépendances manquantes.
    echo 📥 Installation des dépendances...
    pip install -r requirements.txt
    echo ✅ Dépendances installées.
    echo.
)

REM Vérifier le fichier .env
if not exist ".env" (
    echo.
    echo ❌ ERREUR: Fichier .env non trouvé!
    echo.
    echo 📝 Étapes pour corriger:
    echo    1. Dupliquez .env.example en .env
    echo    2. Collez votre TOKEN Discord dans .env
    echo    3. Relancez ce script
    echo.
    pause
    exit /b 1
)

echo ✅ Configuration OK
echo.
echo 🚀 Démarrage du bot...
echo.

REM Lancer le bot
python discord.py

REM Pause pour voir les messages d'erreur
pause