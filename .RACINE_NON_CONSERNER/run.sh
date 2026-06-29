#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════
# SCRIPT DE LANCEMENT - Gestionnaire de Rôles Discord (macOS/Linux)
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo "╔═════════════════════════════════════════════════════════════════════╗"
echo "║     BOT DISCORD - GESTIONNAIRE DE RÔLES                             ║"
echo "║     Démarrage en cours...                                          ║"
echo "╚═════════════════════════════════════════════════════════════════════╝"
echo ""

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "⚠️  Environnement virtuel non trouvé."
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
    echo "✅ Environnement virtuel créé."
    echo ""
fi

# Activer l'environnement virtuel
source venv/bin/activate

# Vérifier si les dépendances sont installées
echo "📋 Vérification des dépendances..."
python -m pip show discord.py > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "⚠️  Dépendances manquantes."
    echo "📥 Installation des dépendances..."
    pip install -r requirements.txt
    echo "✅ Dépendances installées."
    echo ""
fi

# Vérifier le fichier .env
if [ ! -f ".env" ]; then
    echo ""
    echo "❌ ERREUR: Fichier .env non trouvé!"
    echo ""
    echo "📝 Étapes pour corriger:"
    echo "   1. Dupliquez .env.example en .env"
    echo "   2. Collez votre TOKEN Discord dans .env"
    echo "   3. Relancez ce script"
    echo ""
    exit 1
fi

echo "✅ Configuration OK"
echo ""
echo "🚀 Démarrage du bot..."
echo ""

# Lancer le bot
python discord.py