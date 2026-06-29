# 📖 Documentation Technique - Permissions Discord

## 🔐 Comprendre le Bitfield de Permissions

Le Bitfield Discord est une façon efficace de stocker plusieurs permissions dans un **seul entier 64-bit**.

### Concept de Base

Chaque permission a une **valeur de bit** unique :

```
KICK_MEMBERS      = 2^1   = 2      = 0b10
BAN_MEMBERS       = 2^2   = 4      = 0b100
ADMINISTRATOR     = 2^3   = 8      = 0b1000
MANAGE_CHANNELS   = 2^4   = 16     = 0b10000
```

Pour **combiner** des permissions, on utilise l'opérateur binaire OR (`|`) :

```
KICK_MEMBERS (2) | BAN_MEMBERS (4) | ADMINISTRATOR (8) = 14 (0b1110)
```

### Tableau Complet des Permissions

| Permission | Shift | Valeur | Notes |
|------------|-------|--------|-------|
| CREATE_INSTANT_INVITE | 1 << 0 | 1 | Créer des invitations |
| KICK_MEMBERS | 1 << 1 | 2 | Expulser des membres |
| BAN_MEMBERS | 1 << 2 | 4 | Bannir des membres |
| ADMINISTRATOR | 1 << 3 | 8 | 👑 Accès complet |
| MANAGE_CHANNELS | 1 << 4 | 16 | Gérer les salons |
| MANAGE_GUILD | 1 << 5 | 32 | Gérer le serveur |
| ADD_REACTIONS | 1 << 6 | 64 | Ajouter des réactions |
| VIEW_AUDIT_LOG | 1 << 7 | 128 | Voir les logs |
| PRIORITY_SPEAKER | 1 << 8 | 256 | Priorité vocal |
| STREAM | 1 << 9 | 512 | Partager l'écran |
| READ_MESSAGES | 1 << 10 | 1024 | Lire les messages |
| SEND_MESSAGES | 1 << 11 | 2048 | Envoyer des messages |
| SEND_TTS_MESSAGES | 1 << 12 | 4096 | Envoyer en TTS |
| MANAGE_MESSAGES | 1 << 13 | 8192 | Gérer les messages |
| EMBED_LINKS | 1 << 14 | 16384 | Intégrer des liens |
| ATTACH_FILES | 1 << 15 | 32768 | Joindre des fichiers |
| READ_MESSAGE_HISTORY | 1 << 16 | 65536 | Lire l'historique |
| MENTION_EVERYONE | 1 << 17 | 131072 | @everyone/@here |
| USE_EXTERNAL_EMOJIS | 1 << 18 | 262144 | Emojis externes |
| VIEW_GUILD_INSIGHTS | 1 << 19 | 524288 | Analytics serveur |
| CONNECT | 1 << 20 | 1048576 | Se connecter aux vocaux |
| SPEAK | 1 << 21 | 2097152 | Parler en vocal |
| MUTE_MEMBERS | 1 << 22 | 4194304 | Couper les membres |
| DEAFEN_MEMBERS | 1 << 23 | 8388608 | Assourdir les membres |
| MOVE_MEMBERS | 1 << 24 | 16777216 | Déplacer les membres |
| USE_VAD | 1 << 25 | 33554432 | Voice Activity Detection |
| CHANGE_NICKNAME | 1 << 26 | 67108864 | Changer surnom |
| MANAGE_NICKNAMES | 1 << 27 | 134217728 | Gérer surnoms |
| MANAGE_ROLES | 1 << 28 | 268435456 | 🏷️ Gérer les rôles |
| MANAGE_WEBHOOKS | 1 << 29 | 536870912 | Gérer webhooks |
| MANAGE_EMOJIS_AND_STICKERS | 1 << 30 | 1073741824 | Gérer emojis |
| USE_APPLICATION_COMMANDS | 1 << 31 | 2147483648 | Utiliser commandes |
| REQUEST_TO_SPEAK | 1 << 32 | 4294967296 | Demander à parler |
| MANAGE_GUILD_SCHEDULED_EVENTS | 1 << 33 | 8589934592 | Gérer événements |
| MODERATE_MEMBERS | 1 << 40 | 1099511627776 | Modérer membres (timeout) |

## 📚 Ressources

- **discord.py Permissions**: https://discordpy.readthedocs.io/en/stable/api.html#discord.Permissions
- **Discord API Permissions**: https://discord.com/developers/docs/topics/permissions
- **Bitwise Operations**: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Bitwise_OR
- **BigInt JavaScript**: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt

---

**Créé pour le Gestionnaire de Rôles Discord v1.0.0**