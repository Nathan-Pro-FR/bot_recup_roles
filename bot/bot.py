"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                 BOT DISCORD - GESTIONNAIRE DE RÔLES                           ║
║          Exporte et importe les configurations de rôles en JSON               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import discord
from discord.ext import commands
import json
import io
import os
from dotenv import load_dotenv
import pathlib

# Charger les variables d'environnement depuis config/.env si présent,
# sinon laisser load_dotenv gérer la recherche par défaut.
here = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(here)
dotenv_path = os.path.join(project_root, 'config', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    load_dotenv()

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION DES INTENTS
# ═══════════════════════════════════════════════════════════════════════════════
intents = discord.Intents.default()
intents.message_content = True  # Lecture du contenu des messages
intents.guilds = True           # Événements liés aux serveurs

bot = commands.Bot(command_prefix="!", intents=intents)

# ═══════════════════════════════════════════════════════════════════════════════
# ÉVÉNEMENT : BOT PRÊT
# ═══════════════════════════════════════════════════════════════════════════════
@bot.event
async def on_ready():
    """Déclenché quand le bot est connecté et prêt."""
    print(f"✅ Bot connecté en tant que {bot.user.name}")
    print(f"📍 ID: {bot.user.id}")
    print(f"🔧 Commandes disponibles: !exporter_json | !importer_json")

# ═══════════════════════════════════════════════════════════════════════════════
# COMMANDE 1 : EXPORTER_JSON
# ═══════════════════════════════════════════════════════════════════════════════
@bot.command(name="exporter_json")
async def exporter_json(ctx):
    """
    Exporte la configuration brute de tous les rôles du serveur.
    
    Structure JSON générée :
    [
        {
            "id": 12345678901234567890,
            "name": "Admin",
            "position": 10,
            "color": "#ff0000",
            "permissions_value": 8,
            "is_new": false
        },
        ...
    ]
    """
    try:
        serveur = ctx.guild
        
        if not serveur:
            await ctx.send("❌ Erreur : Je ne peux pas récupérer le serveur.")
            return
        
        liste_roles = []
        
        # Parcourir tous les rôles du serveur (trié par position décroissante)
        for role in sorted(serveur.roles, key=lambda r: r.position, reverse=True):
            # Ignorer le rôle par défaut @everyone
            if role.is_default():
                continue
            
            # Construire le dictionnaire du rôle avec les données brutes
            donnees_role = {
                "id": role.id,
                "name": role.name,
                "position": role.position,
                "color": role.color.to_rgb() if role.color else (0, 0, 0),  # Tuple RGB
                "hex_color": str(role.color),  # Format #RRGGBB
                "permissions_value": int(role.permissions.value),  # Bitfield entier
                "is_new": False  # Marquer comme existant (pas nouveau)
            }
            
            liste_roles.append(donnees_role)
        
        # Générer le JSON avec indentation pour lisibilité
        json_text = json.dumps(liste_roles, indent=4, ensure_ascii=False)
        
        # Créer un fichier virtuel en mémoire
        fichier_virtuel = io.BytesIO(json_text.encode('utf-8'))
        
        # Envoyer le fichier dans le canal
        embed = discord.Embed(
            title="📦 Export de Configuration",
            description=f"Rôles exportés : **{len(liste_roles)}**\n\n"
                       f"Utilise `!importer_json` pour importer le fichier modifié.",
            color=discord.Color.green()
        )
        embed.set_footer(text="Gestionnaire de Rôles Discord")
        
        await ctx.send(
            embed=embed,
            file=discord.File(fp=fichier_virtuel, filename="roles_configuration.json")
        )
        
        print(f"✅ {ctx.author.name} a exporté {len(liste_roles)} rôles")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'export: {e}")
        await ctx.send(f"❌ Erreur lors de l'export : `{str(e)}`")

# ═══════════════════════════════════════════════════════════════════════════════
# COMMANDE 2 : IMPORTER_JSON
# ═══════════════════════════════════════════════════════════════════════════════
@bot.command(name="importer_json")
async def importer_json(ctx):
    """
    Importe une configuration de rôles depuis un fichier JSON attaché.
    
    Étapes :
    1. Crée tous les nouveaux rôles (is_new: true)
    2. Applique le bulk edit pour réorganiser les positions
    """
    try:
        # Vérifier qu'un fichier est attaché
        if not ctx.message.attachments:
            await ctx.send("❌ Aucun fichier attaché. Utilise : `!importer_json` + fichier JSON")
            return
        
        # Récupérer le premier fichier attaché
        attachment = ctx.message.attachments[0]
        
        # Vérifier que c'est un fichier JSON
        if not attachment.filename.endswith('.json'):
            await ctx.send("❌ Le fichier doit être au format JSON (.json)")
            return
        
        # Télécharger et parser le JSON
        json_data = await attachment.read()
        roles_config = json.loads(json_data.decode('utf-8'))
        
        serveur = ctx.guild
        statut_message = await ctx.send("⏳ **Traitement en cours...**\n\n")
        
        # ──────────────────────────────────────────────────────────────────────────
        # ÉTAPE 1 : Créer les nouveaux rôles
        # ──────────────────────────────────────────────────────────────────────────
        nouveaux_roles = {}  # {nom: discord.Role}
        roles_crees = 0
        
        for config in roles_config:
            # Vérifier si c'est un rôle à créer
            if config.get("is_new", False):
                try:
                    # Extraire les données du rôle
                    nom = config.get("name", "Rôle Sans Nom")
                    couleur_rgb = config.get("color", (0, 0, 0))
                    permissions_value = config.get("permissions_value", 0)
                    
                    # Convertir les données
                    couleur = discord.Color.from_rgb(*couleur_rgb)
                    permissions = discord.Permissions(permissions_value)
                    
                    # Créer le rôle sur le serveur
                    role = await serveur.create_role(
                        name=nom,
                        color=couleur,
                        permissions=permissions,
                        reason="Création via gestionnaire de rôles"
                    )
                    
                    nouveaux_roles[nom] = role
                    roles_crees += 1
                    
                    print(f"✅ Rôle créé: {nom} (ID: {role.id})")
                    
                except Exception as e:
                    print(f"❌ Erreur lors de la création du rôle {nom}: {e}")
                    await statut_message.edit(content=f"❌ Erreur : impossible de créer '{nom}' : {e}")
                    return
        
                # ──────────────────────────────────────────────────────────────────────────
        # ÉTAPE 2 : Bulk Edit - Réorganiser les positions (Sécurisé)
        # ──────────────────────────────────────────────────────────────────────────
        role_position_map = {}  # {discord.Role: position}
        
        # Récupérer le rôle le plus haut du bot pour ne pas tenter de dépasser ses permissions
        me = serveur.me
        bot_highest_role = me.top_role

        for idx, config in enumerate(roles_config):
            nom = config.get("name")
            position = config.get("position", idx)
            
            # Chercher le rôle : d'abord dans les nouveaux, puis sur le serveur
            role = nouveaux_roles.get(nom)
            if not role:
                role = discord.utils.find(lambda r: r.name == nom, serveur.roles)
            
            if role and not role.is_default():
                # SÉCURITÉ : Le bot ne peut modifier que les rôles STRICTEMENT inférieurs à son rôle max
                if role < bot_highest_role:
                    role_position_map[role] = position
                else:
                    print(f"⚠️ Ignoré (Position trop haute pour le bot) : {nom}")

        # Appliquer le bulk edit en une seule requête
        if role_position_map:
            try:
                await serveur.edit_role_positions(role_position_map)
                print(f"✅ Bulk Edit appliqué : {len(role_position_map)} rôles réorganisés")
            except discord.Forbidden:
                print("❌ Erreur 403 : Le bot n'a pas les permissions requises pour modifier ces positions.")
                await statut_message.edit(content="❌ Erreur : Le rôle du bot est trop bas dans la liste pour déplacer ces rôles.")
                return
            except Exception as e:
                print(f"❌ Erreur lors du bulk edit: {e}")
                await statut_message.edit(content=f"❌ Erreur lors de la réorganisation : {e}")
                return
        else:
            print("⚠️ Aucun rôle réorganisable trouvé.")
        
        # ──────────────────────────────────────────────────────────────────────────
        # CONFIRMATION
        # ──────────────────────────────────────────────────────────────────────────
        embed = discord.Embed(
            title="✅ Import Complété",
            description=f"**Rôles créés :** {roles_crees}\n"
                       f"**Positions réorganisées :** {len(role_position_map)}\n"
                       f"**Rôles totaux sur le serveur :** {len(serveur.roles) - 1}",
            color=discord.Color.green()
        )
        embed.set_footer(text="La hiérarchie a été mise à jour avec succès.")
        
        await statut_message.edit(embed=embed)
        print(f"✅ Import complété par {ctx.author.name}")
        
    except json.JSONDecodeError:
        await ctx.send("❌ Le fichier JSON est invalide ou corrompu.")
        print("❌ Erreur JSON lors de l'import")
    except Exception as e:
        print(f"❌ Erreur lors de l'import: {e}")
        await ctx.send(f"❌ Erreur lors de l'import : `{str(e)}`")

# ═══════════════════════════════════════════════════════════════════════════════
# LANCER LE BOT
# ═══════════════════════════════════════════════════════════════════════════════

# Récupérer le token depuis les variables d'environnement ou .env
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    print("❌ ERREUR : Variable DISCORD_TOKEN non trouvée!")
    print("Crée un fichier .env avec: DISCORD_TOKEN=ton_token_ici")
else:
    try:
        bot.run(TOKEN)
    except discord.errors.PrivilegedIntentsRequired:
        print("❌ ERREUR : Tu dois activer les Privileged Intents dans Discord Developer Portal!")
    except discord.errors.InvalidToken:
        print("❌ ERREUR : Token Discord invalide!")
