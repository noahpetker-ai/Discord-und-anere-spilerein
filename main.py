
import discord
from discord.ext import commands
import os
from datetime import datetime

gespeicherte_notizen = []
gespeicherte_chats = []

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"JJ online als {bot.user}")
    try:
        await bot.tree.sync()
        print("Befehle synchronisiert")
    except Exception as e:
        print(e)

@bot.tree.command(name="jj-help", description="Zeigt alle JJ Befehle")
async def jj_help(interaction: discord.Interaction):
    await interaction.response.send_message("**🤖 JJ Befehle:**\n/jj-help\n/jj-notate [Text]\n/jj-safe\n/jj-print\n/jj-week\n/jj-search [Wort]\n/jj-clear")

@bot.tree.command(name="jj-notate", description="Speichert eine Notiz")
async def jj_notate(interaction: discord.Interaction, text: str):
    gespeicherte_notizen.append(f"{datetime.now().strftime('%d.%m %H:%M')} | {interaction.user.name}: {text}")
    await interaction.response.send_message(f"✅ Gespeichert: {text}")

@bot.tree.command(name="jj-safe", description="Speichert die letzten 7 Nachrichten")
async def jj_safe(interaction: discord.Interaction):
    await interaction.response.defer()
    msgs = [msg async for msg in interaction.channel.history(limit=7)]
    for m in reversed(msgs):
        gespeicherte_chats.append(f"{m.author.name}: {m.content[:200]}")
    await interaction.followup.send(f"✅ {len(msgs)} Nachrichten gespeichert!")

@bot.tree.command(name="jj-print", description="Zeigt alles Gespeicherte")
async def jj_print(interaction: discord.Interaction):
    if not gespeicherte_notizen and not gespeicherte_chats:
        await interaction.response.send_message("Noch nichts gespeichert.")
        return
    alles = "\n".join(gespeicherte_notizen + gespeicherte_chats)
    await interaction.response.send_message(f"**Gespeichert:**\n{alles[-1900:]}")

@bot.tree.command(name="jj-week", description="Zeigt Wochenplan")
async def jj_week(interaction: discord.Interaction):
    await interaction.response.send_message("**📅 Wochenplan:**\nMontag: Zocken 19 Uhr\nDienstag: Clip Review\nMittwoch: Frei\nDonnerstag-Sonntag: Offen")

@bot.tree.command(name="jj-search", description="Sucht live im Chat")
async def jj_search(interaction: discord.Interaction, wort: str):
    await interaction.response.defer()
    gefunden = []
    async for msg in interaction.channel.history(limit=500):
        if wort.lower() in msg.content.lower():
            gefunden.append(f"{msg.author.name}: {msg.content[:100]}")
            if len(gefunden) >= 5:
                break
    if not gefunden:
        await interaction.followup.send(f"Nichts für '{wort}'")
    else:
        await interaction.followup.send(f"**Gefunden:**\n" + "\n".join(gefunden))

@bot.tree.command(name="jj-clear", description="Löscht alles von JJ")
async def jj_clear(interaction: discord.Interaction):
    gespeicherte_notizen.clear()
    gespeicherte_chats.clear()
    await interaction.response.send_message("🗑️ Alles gelöscht!")

bot.run(os.getenv("DISCORD_TOKEN"))
