import os
import random
import discord
from flask import Flask
from threading import Thread

# --- Flask für Render (damit Render nicht meckert) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "JJ ist online! 🔥"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# --- Discord Bot ---
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

custom_commands = {
    "ping": "Pong! JJ ist da! 🎉",
    "moin": "Moin! 👋 Was geht?",
}

@client.event
async def on_ready():
    print(f"JJ ist online! Eingeloggt als {client.user}")

@client.event
async def on_message(message):
    # Ignoriere eigene Nachrichten
    if message.author == client.user:
        return

    text = message.content.lower()

    # --- !hilfe ---
    if text == "!hilfe":
        await message.channel.send(
            "👋 **Hey! Ich bin JJ!**\n\n"
            "Meine Befehle:\n"
            "• `!hilfe` - zeigt diese Hilfe\n"
            "• `!wer bist du` - wer bin ich?\n"
            "• `!jj` - ein Fun-Fact über mich\n"
            "• `!ping` - teste ob ich da bin\n"
            "• `!moin` - sag Moin!\n\n"
            "Oder schreib einfach `hey JJ` 😎"
        )
        return

    # --- !wer bist du ---
    if text == "!wer bist du":
        await message.channel.send(
            "👋 Hey! Ich bin **JJ** - der Bot von dieser Gruppe!\n\n"
            "Ich helfe euch hier, halte den Chat am Laufen und sorge dafür, dass alles smooth läuft. 😎\n\n"
            "Probier doch mal aus:\n"
            "• `!hilfe` - zeigt alle meine Befehle\n"
            "• `!jj` - ein kleiner Fun-Fact über mich\n\n"
            "Schön, dass du da bist! 🙌"
        )
        return

    # --- !jj ---
    if text == "!jj":
        fakten = [
            "Fun-Fact: Ich schlafe nie! 😴❌ Ich bin immer da!",
            "Fun-Fact: Ich bin der coolste Bot in dieser Gruppe! 😎",
            "Fun-Fact: Mein Lieblingsessen ist Code! 🍕💻",
            "Fun-Fact: Ich wurde von Noah gebaut! 🔥",
        ]
        await message.channel.send(random.choice(fakten))
        return

    # --- Hey JJ ---
    if "hey jj" in text or "hey, jj" in text or "heyy jj" in text:
        antworten = [
            "Heyy! 👋 Da bin ich! Was geht?",
            "Jo, ich bin da! 😎 Was brauchst du?",
            "Hey! 🙌 Schön dich zu sehen! Was gibt's?",
            "Ja bitte? 😄 Ich höre!",
            "Hey hey! 🔥 Erzähl mal, was los ist?",
        ]
        await message.channel.send(random.choice(antworten))
        return

    # --- Custom Commands wie !ping, !moin ---
    if text.startswith("!"):
        befehl = text[1:].split()[0]
        if befehl in custom_commands:
            await message.channel.send(custom_commands[befehl])
            return

# --- Start ---
if __name__ == "__main__":
    # Flask im Hintergrund starten
    Thread(target=run_flask, daemon=True).start()
    # Discord Bot starten
    token = os.environ.get("DISCORD_TOKEN")
    client.run(token)
