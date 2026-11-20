import os
import json
from flask import Flask, request, redirect, render_template_string, session
from threading import Thread
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "JJ123")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0")) # ID von #allgemein

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Befehle die man im Admin-Bereich erstellen kann
# Format: {"witz": "Dein Witz-Text"}
custom_commands = {
    "ping": "Pong! JJ ist da! 🎉",
    "moin": "Moin!",
}

if message.content.lower() == "!wer bist du":
    await message.channel.send(
        "👋 Hey! Ich bin **JJ** - der Bot von dieser Gruppe!\n\n"
        "Ich helfe euch hier, halte den Chat am Laufen und sorge dafür, dass alles smooth läuft. 😎\n\n"
        "Probier doch mal aus:\n"
        "• `!hilfe` - zeigt alle meine Befehle\n"
        "• `!jj` - ein kleiner Fun-Fact über mich\n\n"
        "Schön, dass du da bist! 🙌"
    )

if "hey jj" in message.content.lower() or "hey, jj" in message.content.lower() or "heyy jj" in message.content.lower():
    antworten = [
        "Heyy! 👋 Da bin ich! Was geht?",
        "Jo, ich bin da! 😎 Was brauchst du?",
        "Hey! 🙌 Schön dich zu sehen! Was gibt's?",
        "Ja bitte? 😄 Ich höre!",
        "Hey hey! 🔥 Erzähl mal, was los ist?",
    ]
    await message.channel.send(random.choice(antworten))


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "jj-secret-123")

HTML = """
<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>JJ Control</title>
<style>
body{font-family:Arial;background:#1a1a2e;color:white;padding:20px;max-width:600px;margin:auto}
.card{background:#16213e;padding:20px;border-radius:15px;margin:15px 0}
button,input,textarea,select{width:100%;padding:12px;margin:8px 0;border-radius:10px;border:none;font-size:16px}
button{background:#7289da;color:white;font-weight:bold;cursor:pointer}
input,textarea,select{background:#0f3460;color:white}
.admin{background:#3a0a0a;border:1px solid #ff5555}
.badge{padding:5px 10px;border-radius:20px;background:green}
a{color:#7289da}
</style></head><body>
<h1>🤖 JJ Control</h1>
<p>Status: <span class="badge">{{status}}</span> | Befehle: {{cmds}}</p>

<div class="card">
<h2>👋 Besucher-Bereich</h2>
<h3>1. Befehl ausführen</h3>
<form action="/run" method="post">
<select name="cmd">{% for c in cmds_list %}<option value="{{c}}">!{{c}}</option>{% endfor %}</select>
<button>▶️ In Discord ausführen</button>
</form>

<h3>2. Eigene Nachricht designen</h3>
<form action="/send" method="post">
<textarea name="text" placeholder="Deine Nachricht an #allgemein..." required></textarea>
<select name="style">
<option value="normal">Normal</option>
<option value="fett">**FETT**</option>
<option value="party">🎉 Party 🎉</option>
<option value="warnung">⚠️ Wichtig ⚠️</option>
</select>
<button>📨 An Discord senden</button>
</form>
<p>{{msg}}</p>
</div>

<div class="card admin">
<h2>🔐 Admin-Bereich</h2>
{% if is_admin %}
<p>✅ Du bist eingeloggt als Admin</p>
<h3>Neuen Befehl erstellen</h3>
<form action="/admin/add" method="post">
<input name="name" placeholder="Befehlsname ohne ! z.B. witz" required>
<textarea name="text" placeholder="Was soll JJ antworten?" required></textarea>
<button>➕ Befehl speichern</button>
</form>
<h3>Alle Befehle</h3>
<ul>{% for c in cmds_list %}<li>!{{c}} - <a href="/admin/del/{{c}}">Löschen</a></li>{% endfor %}</ul>
<a href="/logout">Ausloggen</a>
{% else %}
<form action="/login" method="post">
<input type="password" name="pw" placeholder="Admin-Passwort" required>
<button>🔓 Einloggen</button>
</form>
{% endif %}
</div>
</body></html>
"""

def get_channel():
    if CHANNEL_ID:
        return bot.get_channel(CHANNEL_ID)
    # Fallback: erster Textkanal namens allgemein
    for g in bot.guilds:
        for ch in g.text_channels:
            if ch.name == "allgemein":
                return ch
    return None

@app.route("/")
def home():
    status = "🟢 ONLINE" if bot.is_ready() else "🔴 OFFLINE / Schläft - Seite neu laden"
    return render_template_string(HTML, status=status, cmds=len(custom_commands), cmds_list=list(custom_commands.keys()), is_admin=session.get("admin", False), msg=request.args.get("msg",""))

@app.route("/run", methods=["POST"])
def run_cmd():
    cmd = request.form.get("cmd")
    ch = get_channel()
    if ch and cmd in custom_commands:
        bot.loop.create_task(ch.send(custom_commands[cmd]))
        return redirect("/?msg=✅ !"+cmd+" wurde in Discord ausgeführt!")
    return redirect("/?msg=❌ Bot nicht bereit, Webseite neu laden!")

@app.route("/send", methods=["POST"])
def send_msg():
    text = request.form.get("text","")
    style = request.form.get("style","normal")
    if style == "fett":
        text = f"**{text}**"
    elif style == "party":
        text = f"🎉🎉 {text} 🎉🎉"
    elif style == "warnung":
        text = f"⚠️ **WICHTIG:** {text}"
    ch = get_channel()
    if ch:
        bot.loop.create_task(ch.send(text))
        return redirect("/?msg=✅ Nachricht gesendet!")
    return redirect("/?msg=❌ Bot nicht bereit!")

@app.route("/login", methods=["POST"])
def login():
    if request.form.get("pw") == ADMIN_PASSWORD:
        session["admin"] = True
    return redirect("/")

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")

@app.route("/admin/add", methods=["POST"])
def admin_add():
    if not session.get("admin"):
        return redirect("/")
    name = request.form.get("name","").lower().strip().replace("!","").replace(" ","")
    text = request.form.get("text","")
    if name and text:
        custom_commands[name] = text
    return redirect("/?msg=✅ Befehl !"+name+" erstellt!")

@app.route("/admin/del/<name>")
def admin_del(name):
    if not session.get("admin"):
        return redirect("/")
    if name in custom_commands and name not in ["ping","moin"]:
        del custom_commands[name]
    return redirect("/")

# Discord Befehle - dynamisch
@bot.event
async def on_ready():
    print(f"JJ ist online als {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.startswith("!"):
        name = message.content[1:].split(" ")[0].lower()
        if name in custom_commands:
            await message.channel.send(custom_commands[name])
            return
    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send(custom_commands.get("ping", "Pong!"))

@bot.command()
async def moin(ctx):
    await ctx.send(custom_commands.get("moin", "Moin!"))

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.run(TOKEN)
