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

## 🧮 Calculs Pratiques

### Exemple 1: Créer un Modérateur

```python
KICK_MEMBERS = 2              # 1 << 1
BAN_MEMBERS = 4               # 1 << 2
MANAGE_MESSAGES = 8192        # 1 << 13
MUTE_MEMBERS = 4194304        # 1 << 22
MANAGE_ROLES = 268435456      # 1 << 28

bitfield = 2 | 4 | 8192 | 4194304 | 268435456
         = 268438370  # ← Valeur finale
```

### Exemple 2: Administrateur Complet

```python
# Simplement: ADMINISTRATOR = 8
# Cela accorde TOUS les droits automatiquement
bitfield = 8
```

### Exemple 3: Vérifier une Permission

Pour vérifier si un rôle a la permission `MANAGE_ROLES (268435456)` :

```python
bitfield = 268438370
MANAGE_ROLES = 268435456

has_permission = (bitfield & MANAGE_ROLES) != 0
# has_permission = True ✅
```

## 🔀 Opérations Binaires

### OR (|) - Ajouter une Permission
```python
current = 2        # KICK_MEMBERS
add = 4            # BAN_MEMBERS
result = current | add
# result = 6 (KICK_MEMBERS + BAN_MEMBERS)
```

### AND (&) - Tester une Permission
```python
bitfield = 14      # KICK + BAN + ADMIN
test = 8           # ADMINISTRATOR
has_it = (bitfield & test) != 0
# has_it = True ✅
```

### XOR (^) - Basculer une Permission
```python
bitfield = 14      # KICK + BAN + ADMIN
toggle = 4         # BAN_MEMBERS
result = bitfield ^ toggle
# result = 10 (KICK + ADMIN, BANs'il était présent est retiré)
```

## 💻 Code JavaScript (Calcul BigInt)

L'interface web utilise **BigInt** pour garantir la précision :

```javascript
// Initialisation des permissions
const permissions = {
    'KICK_MEMBERS': 1n << 1n,           // 2
    'BAN_MEMBERS': 1n << 2n,             // 4
    'ADMINISTRATOR': 1n << 3n,           // 8
    'MANAGE_ROLES': 1n << 28n,           // 268435456
    // ...
};

// Calculer le bitfield
function calculateBitfield(selectedPermissions) {
    let bitfield = 0n;
    selectedPermissions.forEach(perm => {
        bitfield |= permissions[perm];  // OR binaire
    });
    return Number(bitfield);  // Convertir en nombre normal
}

// Exemple
const selected = ['KICK_MEMBERS', 'BAN_MEMBERS', 'MANAGE_ROLES'];
const bitfield = calculateBitfield(selected);
console.log(bitfield);  // 268435462
```

## 🐍 Code Python (discord.py)

```python
# Créer un rôle avec des permissions
role = await guild.create_role(
    name="Modérateur",
    permissions=discord.Permissions(
        kick_members=True,
        ban_members=True,
        manage_messages=True,
        manage_roles=True,
        moderate_members=True
    ),
    color=discord.Color.blue()
)

# Ou avec un bitfield direct
role = await guild.create_role(
    name="Modérateur",
    permissions=discord.Permissions(268438370),  # Bitfield calculé
    color=discord.Color.blue()
)

# Vérifier une permission
if role.permissions.manage_roles:
    print("✅ Peut gérer les rôles")

# Obtenir la valeur numérique
print(role.permissions.value)  # 268438370
```

## 📊 Cas d'Usage Courants

### Rôle "Modérateur Complet"
```
Permissions:
- Kick Members
- Ban Members
- Manage Messages
- Manage Roles (si possible)
- Mute Members
- Moderate Members (timeout)

Bitfield: 2 + 4 + 8192 + 268435456 + 4194304 + 1099511627776
       = 1099523836734
```

### Rôle "Utilisateur Normal"
```
Permissions:
- Send Messages
- Read Message History
- Connect (voice)
- Speak (voice)

Bitfield: 2048 + 65536 + 1048576 + 2097152
       = 3211312
```

### Rôle "Support/Helper"
```
Permissions:
- Send Messages
- Manage Messages
- Mute Members
- Read Message History

Bitfield: 2048 + 8192 + 4194304 + 65536
       = 4270080
```

## 🚀 Optimisations

### BigInt pour Éviter les Pertes

En JavaScript, les nombres au-delà de 2^53 - 1 perdent en précision. Donc :

```javascript
// ❌ MAUVAIS - Perte de précision
const bitfield = 1099511627776;
console.log(bitfield);  // 1099511627776 (perte de précision possible)

// ✅ BON - BigInt
const bitfield = 1n << 40n;
console.log(Number(bitfield));  // 1099511627776 (précision garantie)
```

### Bulk Edit pour la Performance

Au lieu de modifier les positions rôle par rôle :

```python
# ❌ LENT - Plusieurs requêtes
for role in roles:
    await role.edit(position=new_position)  # N requêtes

# ✅ RAPIDE - Une seule requête
role_positions = {
    role1: 5,
    role2: 4,
    role3: 3
}
await guild.edit_role_positions(role_positions)  # 1 requête!
```

## 📚 Références

- **discord.py Permissions**: https://discordpy.readthedocs.io/en/stable/api.html#discord.Permissions
- **Discord API Permissions**: https://discord.com/developers/docs/topics/permissions
- **Bitwise Operations**: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Bitwise_OR
- **BigInt JavaScript**: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt

---

**Créé pour le Gestionnaire de Rôles Discord v1.0.0**