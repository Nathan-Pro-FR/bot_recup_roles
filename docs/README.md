# 🎭 Gestionnaire de Rôles Discord

Écosystème complet pour gérer les rôles de votre serveur Discord de manière visuelle et intuitive. Parfait pour les serveurs avec 60 à 160+ rôles.

## 📋 Fonctionnalités

### 🤖 BOT DISCORD (Back-end)

- **`!exporter_json`** : Exporte tous les rôles du serveur dans un fichier `roles_configuration.json`
  - Capture : ID, nom, position, couleur (RGB/Hex), permissions (bitfield)
  - Envoie le fichier directement dans le salon

- **`!importer_json`** : Importe un fichier JSON modifié et :
  - Crée automatiquement les nouveaux rôles (`is_new: true`)
  - Applique un **bulk edit** pour réorganiser les positions en une seule requête API
  - Préserve tous les rôles existants (zéro risque d'écrasement)

### 🌐 INTERFACE WEB (Front-end)

- 📥 **Importation** : Chargez le fichier JSON exporté
- 🎯 **Tri tactile** : Boutons ↑ ↓ pour déplacer les rôles (mobile-friendly)
- ✨ **Création** : Modal pour créer des rôles avec :
  - Nom personnalisé
  - Sélecteur de couleur
  - Liste complète des permissions Discord
  - Calculateur de bitfield **64-bit BigInt** (sécurisé)
- 📤 **Export** : Télécharge le JSON modifié prêt pour le bot
- 📊 **Statistiques** : Affiche les totaux de rôles, permissions, nouveaux rôles

## 🚀 Installation Rapide

Lisez [QUICKSTART.txt](QUICKSTART.txt) pour un guide en 5 minutes.

---

**Créé avec ❤️ pour les gestionnaires de serveurs Discord**  
Version: **1.0.0** | Dernière mise à jour: **28 Juin 2024**