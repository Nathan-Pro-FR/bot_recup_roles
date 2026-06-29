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

### Prérequis

- **Python 3.9+** (pour le bot)
- **discord.py 2.0+**
- **Un navigateur moderne** (Chrome, Firefox, Safari, Edge)
- **Un serveur Discord** et **droits administrateur**

### Étape 1 : Configuration du Bot Discord

1. **Créer une application Discord**
   - Allez sur [Discord Developer Portal](https://discord.com/developers/applications)
   - Cliquez sur "New Application"
   - Nommez-la (ex: "Role Manager")

2. **Créer un bot**
   - Onglet "Bot" → "Add Bot"
   - Copiez le **TOKEN** (gardez-le secret!)

3. **Activer les Privileged Intents**
   - Onglet "Bot" → "Privileged Gateway Intents"
   - ✅ Activez : **Message Content Intent**, **Server Members Intent**, **Guilds**

4. **Créer une URL d'invitation**
   - Onglet "OAuth2" → "URL Generator"
   - Scopes : `bot`
   - Permissions :
     - ✅ Manage Guild
     - ✅ Manage Roles
     - ✅ View Audit Log
     - ✅ Send Messages
   - Copiez l'URL et invitez le bot sur votre serveur

### Étape 2 : Installation des Dépendances

```bash
# Se placer dans le dossier du projet
cd d:\PERSONNEL\bot_recup_roles

# Créer un environnement virtuel (recommandé)
python -m venv venv

# Activer l'environnement
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Installer discord.py et python-dotenv
pip install discord.py python-dotenv
```

### Étape 3 : Configurer le Token

1. **Dupliquez le fichier** `.env.example` → `.env`
2. **Collez votre TOKEN Discord** dans le fichier `.env` :

```env
DISCORD_TOKEN=votre_token_ici
```

⚠️ **JAMAIS** de token en dur dans le code !

### Étape 4 : Lancer le Bot

```bash
python discord.py
```

Vous devriez voir :
```
✅ Bot connecté en tant que [BotName]
📍 ID: 123456789
🔧 Commandes disponibles: !exporter_json | !importer_json
```

### Étape 5 : Utiliser l'Interface Web

1. **Ouvrez `index.html`** dans votre navigateur (double-clic ou glissez-déposez)
2. **Sur Discord**, exécutez : `!exporter_json`
3. **Téléchargez** le fichier `roles_configuration.json`
4. **Dans l'interface web**, cliquez sur "📥 Importer JSON"
5. **Modifiez** les rôles à votre guise
6. **Cliquez** sur "📤 Exporter JSON Modifié"
7. **Sur Discord**, exécutez : `!importer_json` + attachez le fichier modifié

## 📱 Utilisation Complète

### Workflow Complet

```
Discord Server
      ↓
!exporter_json (Bot)
      ↓
roles_configuration.json (Télécharge)
      ↓
Web Interface (Importez)
      ↓
[Modifiez les rôles]
      ↓
Export JSON modifié
      ↓
!importer_json (Bot + fichier)
      ↓
Discord Server [Mis à jour]
```

### Cas d'Usage

#### 1️⃣ Réorganiser les Rôles Existants
- Export → Web UI (glissez-déposez)
- Import → Bot applique les nouvelles positions

#### 2️⃣ Créer de Nouveaux Rôles en Masse
- Web UI → Cliquez "✨ Créer un Rôle"
- Remplissez nom, couleur, permissions
- Export → Import au bot
- Les nouveaux rôles sont créés + insérés à la bonne position

#### 3️⃣ Copier une Configuration
- Export depuis un serveur
- Import sur un autre serveur Discord
- Tous les rôles (nouveaux) sont répliqués

## 🔐 Sécurité

✅ **Aucun risque pour votre serveur**
- ✅ Les rôles existants ne sont **jamais** supprimés
- ✅ Seules les **nouvelles positions** sont appliquées
- ✅ Les **nouveaux rôles** sont créés en bas de la hiérarchie
- ✅ **Bulk edit** = une seule requête API = pas de race conditions

✅ **Token sécurisé**
- ✅ Fichier `.env` ignoré par Git (dans `.gitignore`)
- ✅ Jamais exposé dans le code

✅ **Permissions bitfield**
- ✅ Utilise **BigInt 64-bit** (JavaScript) pour éviter les pertes de précision
- ✅ Calculé correctement selon l'API Discord

## 📊 Structure JSON

### Format d'Export

```json
[
    {
        "id": 1104570726405320733,
        "name": "Admin",
        "position": 10,
        "color": [88, 101, 242],
        "hex_color": "#5865f2",
        "permissions_value": 8,
        "is_new": false
    },
    {
        "id": 1234567890123456789,
        "name": "Modérateur",
        "position": 9,
        "color": [255, 0, 0],
        "hex_color": "#ff0000",
        "permissions_value": 134217728,
        "is_new": true
    }
]
```

### Champs Expliqués

| Champ | Type | Exemple | Notes |
|-------|------|---------|-------|
| `id` | Entier | 1104570726405320733 | ID unique du rôle Discord |
| `name` | Texte | "Admin" | Nom du rôle |
| `position` | Entier | 10 | Position dans la hiérarchie (0 = bas) |
| `color` | Array RGB | [88, 101, 242] | Couleur RGB (0-255 chacun) |
| `hex_color` | Texte | "#5865f2" | Couleur hexadécimale |
| `permissions_value` | Entier | 8 | Bitfield Discord (union de permissions) |
| `is_new` | Booléen | true/false | Indique si le rôle doit être créé |

### Calcul du Bitfield

Chaque permission Discord a une valeur de bit :

```
ADMINISTRATOR     = 8 (1 << 3)
MANAGE_GUILD      = 32 (1 << 5)
MANAGE_CHANNELS   = 16 (1 << 4)
MANAGE_ROLES      = 268435456 (1 << 28)
BAN_MEMBERS       = 4 (1 << 2)
KICK_MEMBERS      = 2 (1 << 1)
```

Pour combiner : `8 | 32 | 16 = 56` → Permissions : ADMINISTRATOR + MANAGE_GUILD + MANAGE_CHANNELS

## 🛠️ Dépannage

### ❌ Le bot n'apparaît pas en ligne
- ✅ Vérifiez que le **TOKEN** est correct dans `.env`
- ✅ Vérifiez les **Privileged Intents** activés
- ✅ Vérifiez que le bot est **invité** sur le serveur

### ❌ `Command raised an exception: PrivilegedIntentsRequired`
- ✅ Allez dans Discord Developer Portal
- ✅ Bot → **Privileged Gateway Intents**
- ✅ Activez **Message Content Intent**
- ✅ Redémarrez le bot

### ❌ `roles_configuration.json` vide ou erreur JSON
- ✅ Vérifiez que le serveur **a des rôles** (autres que @everyone)
- ✅ Exécutez `!exporter_json` à nouveau

### ❌ L'interface web ne charge pas les couleurs
- ✅ Le JSON doit avoir le champ `color` (array RGB) OU `hex_color`
- ✅ Les deux sont générés automatiquement par le bot

## 💡 Astuces

### Pour les Gros Serveurs (160+ rôles)
- Utilisez **plusieurs fichiers JSON** (par catégorie)
- Fusionnez-les manuellement ou via un script
- Les positions se recalculent automatiquement

### Sauvegardes
- Gardez toujours une **copie du JSON d'origine** avant de modifier
- Versionnez vos configurations : `roles_backup_2024_06_28.json`

### Performance
- Fermez l'interface web si vous n'en avez pas besoin
- Le bot utilise les **Intents minimaux** requis
- Les **bulk edits** sont **infiniment** plus rapides qu'éditer rôle par rôle

## 📚 Ressources Importantes

- **discord.py Docs** : https://discordpy.readthedocs.io/
- **Discord API** : https://discord.com/developers/docs
- **Permissions** : https://discord.com/developers/docs/topics/permissions
- **BigInt JavaScript** : https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt

## 📝 Licence

Ce projet est fourni à titre d'exemple. Utilisez-le librement sur vos serveurs Discord.

## 🤝 Support

Pour toute question :
1. Vérifiez les logs du bot (console)
2. Vérifiez la console du navigateur (F12 → Console)
3. Relisez le fichier `.env` et permissions Discord Developer Portal

---

**Créé avec ❤️ pour les gestionnaires de serveurs Discord**

Version: **1.0.0**
Dernière mise à jour: **28 Juin 2024**