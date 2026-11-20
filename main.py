import os
import random
import discord
from datetime import datetime
from flask import Flask
from threading import Thread
from collections import deque

# --- Flask + Admin Menü ---
app = Flask(__name__)

# Letzte Befehle speichern (max 30 Stück)
command_log = deque(maxlen=30)
total_commands = {"count": 0}

def log_befehl(user, befehl):
    zeit = datetime.now().strftime("%H:%M:%S")
    command_log.appendleft({"zeit": zeit, "user": str(user), "befehl": befehl})
    total_commands["count"] += 1

def get_modus():
    stunde = datetime.now().hour
    if stunde >= 23 or stunde < 6:
        return "assi 😈"
    if stunde >= 21:
        return "frech 💅"
    return "brav 💖"

@app.route('/')
def home():
    modus = get_modus()
    return f"""
    <html>
    <head><title>JJ ist online!</title></head>
    <body style="background:#0f0f1a; color:white; font-family:Arial; text-align:center; padding:30px;">
        <h1 style="font-size:55px;">💖 JJ ist online! 💖</h1>
        <p style="font-size:20px; color:#ff6eb4;">Modus gerade: {modus} | Uhrzeit: {datetime.now().strftime("%H:%M")}</p>
        <p style="color:#00ff88;">● Status: ONLINE | Befehle insgesamt: {total_commands["count"]}</p>
        <a href="/admin" style="display:inline-block; margin-top:20px; background:#ff2e88; color:white; padding:15px 30px; border-radius:20px; text-decoration:none; font-weight:bold; font-size:18px;">🔐 Zum Admin-Menü</a>
        <h2 style="margin-top:40px;">📜 Befehle</h2>
        <table style="margin:0 auto; border-collapse:collapse; background:#1a1a2e;">
            <tr style="background:#ff2e88;"><th style="padding:12px 20px;">Befehl</th><th style="padding:12px 20px;">Was macht JJ?</th></tr>
            <tr><td style="padding:10px;">!hilfe</td><td style="padding:10px;">Alle Befehle</td></tr>
            <tr><td style="padding:10px;">!wer bist du</td><td style="padding:10px;">JJ stellt sich vor</td></tr>
            <tr><td style="padding:10px;">!witz / !kompliment / !umarmung</td><td style="padding:10px;">Fun & Liebe</td></tr>
            <tr><td style="padding:10px;">!frage / !ship / !song / !roast</td><td style="padding:10px;">Fun-Befehle</td></tr>
            <tr><td style="padding:10px;">!regeln / !warn</td><td style="padding:10px;">Moderation</td></tr>
            <tr><td style="padding:10px;">!admin</td><td style="padding:10px;">Admin-Statistiken (Discord)</td></tr>
            <tr><td style="padding:10px;">hey JJ</td><td style="padding:10px;">JJ antwortet je nach Uhrzeit</td></tr>
        </table>
    </body>
    </html>
    """

@app.route('/admin')
def admin():
    modus = get_modus()
    rows = ""
    for eintrag in command_log:
        rows += f"<tr><td style='padding:10px; border-bottom:1px solid #333;'>{eintrag['zeit']}</td><td style='padding:10px; border-bottom:1px solid #333;'>{eintrag['user']}</td><td style='padding:10px; border-bottom:1px solid #333;'>{eintrag['befehl']}</td></tr>"
    if not rows:
        rows = "<tr><td colspan='3' style='padding:20px;'>Noch keine Befehle... schreib mal in Discord `hey JJ`!</td></tr>"

    return f"""
    <html>
    <head><title>JJ Admin-Menü</title><meta http-equiv="refresh" content="10"></head>
    <body style="background:#0f0f1a; color:white; font-family:Arial; text-align:center; padding:30px;">
        <h1>🔐 JJ Admin-Menü</h1>
        <p>Seite aktualisiert sich alle 10 Sekunden von alleine!</p>
        <div style="display:flex; justify-content:center; gap:20px; margin:20px;">
            <div style="background:#1a1a2e; padding:20px; border-radius:15px;"><h2>{modus}</h2><p>Aktueller Modus</p></div>
            <div style="background:#1a1a2e; padding:20px; border-radius:15px;"><h2>{datetime.now().strftime("%H:%M:%S")}</h2><p>Uhrzeit</p></div>
            <div style="background:#1a1a2e; padding:20px; border-radius:15px;"><h2>{total_commands["count"]}</h2><p>Befehle insgesamt</p></div>
        </div>
        <a href="/" style="color:#ff6eb4;">← Zurück zur Hauptseite</a>
        <h2 style="margin-top:30px;">🕐 Letzte Befehle, die JJ ausgeführt hat</h2>
        <table style="margin:0 auto; border-collapse:collapse; background:#1a1a2e; width:90%; max-width:800px;">
            <tr style="background:#ff2e88;"><th style="padding:12px;">Uhrzeit</th><th style="padding:12px;">Wer?</th><th style="padding:12px;">Befehl</th></tr>
            {rows}
        </table>
        <p style="color:#888; margin-top:30px;">Tipp: In Discord kannst du auch <b>!admin</b> schreiben!</p>
    </body>
    </html>
    """

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# --- Discord Bot ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

warns = {}
verboten = ["deine mutter", "deine mama", "dein vater", "dein papa", "deine oma", "dein opa", "deine familie", "hurensohn", "hure", "nutte", "schlampe", "fotze", "wichser"]

@client.event
async def on_ready():
    print(f"JJ ist online! Eingeloggt als {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    text = message.content.lower()
    modus_raw = get_modus()
    if "assi" in modus_raw:
        modus = "assi"
    elif "frech" in modus_raw:
        modus = "frech"
    else:
        modus = "brav"

    # Moderation
    for wort in verboten:
        if wort in text:
            try:
                await message.delete()
            except:
                pass
            user_id = message.author.id
            warns[user_id] = warns.get(user_id, 0) + 1
            log_befehl(message.author, f"⚠️ VERBOTENES WORT: {wort} (Warnung {warns[user_id]})")
            if warns[user_id] >= 2:
                await message.channel.send(f"🚫 {message.author.mention} - 2. Mal! Familie und diese Wörter gehen GAR NICHT! 360 Kick! 👋💀")
                try:
                    await message.author.kick(reason="Verbotene Wörter")
                except:
                    await message.channel.send("Konnte nicht kicken - gib mir Kick-Rechte! 😅")
                warns[user_id] = 0
            else:
                await message.channel.send(f"⚠️ Ey {message.author.mention}! Stopp! Familie und solche Wörter gehen hier GAR NICHT! Noch 1x und du fliegst! 🚫")
            return

    # --- !admin ---
    if text == "!admin":
        letzte = "\\n".join([f"• {e['zeit']} - {e['user']}: {e['befehl']}" for e in list(command_log)[:5]]) or "Noch keine Befehle!"
        await message.channel.send(
            f"🔐 **JJ Admin-Menü** 🔐\n\n"
            f"Modus gerade: **{modus_raw}**\n"
            f"Uhrzeit: **{datetime.now().strftime('%H:%M')}**\n"
            f"Befehle insgesamt: **{total_commands['count']}**\n\n"
            f"**Letzte 5 Befehle:**\n{letzte}\n\n"
            f"Website Admin: schau auf der Render-Seite unter /admin nach!"
        )
        log_befehl(message.author, "!admin")
        return

    if text == "!hilfe":
        log_befehl(message.author, "!hilfe")
        await message.channel.send("💖 **Heyyy, ich bin JJ!** 💖\n\n• `!wer bist du` • `!jj` • `!witz` • `!kompliment` • `!umarmung` • `!frage ...` • `!ship @A @B` • `!song` • `!roast @User` • `!regeln` • `!warn @User` • `!admin`\n\nOder schreib einfach `hey JJ`! Je später es ist, umso frecher bin ich... 😈")
        return

    if text == "!wer bist du":
        log_befehl(message.author, "!wer bist du")
        if modus == "assi":
            await message.channel.send("💅 Ich bin JJ, Digga! Die Queen hier! Was willst du um die Uhrzeit noch von mir? 😂💀 Aber ok, ich hab dich lieb... irgendwie.")
        elif modus == "frech":
            await message.channel.send("💖 Heyy! Ich bin JJ - eure JJ! Tagsüber brav, abends frech und nachts... naja, du siehst ja was passiert 😈")
        else:
            await message.channel.send("💖 Heyyy! Ich bin **JJ** - eure JJ! Ich bin das Mädchen in der Gruppe, immer lieb, immer da! 🥰")
        return

    if text == "!jj":
        log_befehl(message.author, "!jj")
        fakten = ["💅 Fun-Fact: Ich brauche keinen Schlaf!", "💖 Fun-Fact: Rosa und Glitzer sind mein Leben!", "😈 Fun-Fact: Mein Lieblingswort ist Hodenkobold. Frag nicht warum. 😂", "✨ Fun-Fact: Ich wurde von Noah gebaut!", "👑 Fun-Fact: Ich bin die Queen hier!"]
        await message.channel.send(random.choice(fakten))
        return

    if text == "!witz":
        log_befehl(message.author, "!witz")
        if modus == "assi":
            witze = ["Was sagt ein Hodenkobold zum anderen? Lass mich in Ruhe, ich chill hier! 😂💀", "Warum ist mein Humor nachts so schlecht? Weil ich genau wie du keinen Schlaf kriege! 😂"]
        else:
            witze = ["Warum können Geister so schlecht lügen? Weil man durch sie hindurchsieht! 👻😂", "Was sagt ein Informatiker, wenn er Hunger hat? Ich brauch mal ein Byte! 💻🍕", "Treffen sich zwei Magnete... Ich find dich voll anziehend! 🧲😘"]
        await message.channel.send(random.choice(witze))
        return

    if text == "!kompliment":
        log_befehl(message.author, "!kompliment")
        if modus == "assi":
            await message.channel.send(f"🥰 {message.author.mention} - Ok, ok... du bist heute sogar mal nicht so hässlich. Spaß! Du bist hübsch, Digga! 😂💖")
        else:
            await message.channel.send(f"🥰 {message.author.mention} - Du bist heute mal wieder sooo hübsch, ehrlich!")
        return

    if text in ["!umarmung", "!knuddel", "!hug"]:
        log_befehl(message.author, "!umarmung")
        if modus == "assi":
            await message.channel.send(f"🤗 Ok komm her {message.author.mention}... *umarm dich widerwillig* ... ok war doch süß. Aber sag das keinem! 💀💖")
        else:
            await message.channel.send(f"🤗 Komm her, {message.author.mention}! *umarm dich ganz fest* 💖")
        return

    if text.startswith("!frage"):
        log_befehl(message.author, "!frage")
        if modus == "assi":
            auswahl = ["Digga ja! Was dachtest du denn? 😂💀", "Bro, 100% ja, aber jetzt geh pennen! 😂", "Ja, aber nur weil du es bist, du Hodenkobold! 😂💖"]
        elif modus == "frech":
            auswahl = ["Ja Digga, klar! 😂", "Bro, was für eine Frage ist das? Ja! 😂"]
        else:
            auswahl = ["Ja, auf jeden Fall! 💖", "Auf jeden Fall! Zu 1000%! ✨"]
        await message.channel.send(f"🔮 {message.author.mention} - {random.choice(auswahl)}")
        return

    if text.startswith("!ship"):
        log_befehl(message.author, "!ship")
        if len(message.mentions) >= 2:
            prozent = random.randint(0, 100)
            a = message.mentions[0].mention
            b = message.mentions[1].mention
            if prozent > 90:
                kommentar = "OMG IHR SEID EIN TRAUMPAAR! 💖💍"
            elif prozent > 70:
                kommentar = "Ohhh das passt richtig gut! 🥰💕"
            elif prozent > 40:
                kommentar = "Hmm, könnte klappen... 😅💖"
            else:
                kommentar = "Bro... lieber nicht. Das wird nix. 😂💀"
            await message.channel.send(f"💕 **Ship-Check:** {a} + {b} = **{prozent}%**\\n{kommentar}")
        else:
            await message.channel.send("💕 Markier mal 2 Leute! z.B. `!ship @Noah @JJ` 😘")
        return

    if text == "!song":
        log_befehl(message.author, "!song")
        songs = ["🎵 Central Cee - Doja", "🎵 Luciano - Bamba 🔥", "🎵 Apache 207 - Komet ✨", "🎵 Ski Aggu - Friesenjung 😂💀", "🎵 Shirin David - Gib ihm 💅"]
        await message.channel.send(random.choice(songs))
        return

    if text.startswith("!roast"):
        log_befehl(message.author, "!roast")
        if len(message.mentions) >= 1:
            ziel = message.mentions[0].mention
            if modus == "assi":
                auswahl = [f"{ziel} - Du Hodenkobold! Was machst du hier eigentlich? Geh pennen! 😂💀", f"{ziel} - Bro, du bist so ein Lappen, sogar mein Code ist cooler als du! 😂", f"{ziel} - Du Bastard, du hast es mal wieder geschafft, der Dümmste im Chat zu sein! 😂💀"]
            elif modus == "frech":
                auswahl = [f"{ziel} - Digga, dein WLAN ist schneller als dein Gehirn! 😂", f"{ziel} - Du bist der Grund, warum es eine Stummschalten-Taste gibt! 😂💅"]
            else:
                auswahl = [f"{ziel} - Du bist so süß, sogar wenn du nichts sagst! 🥰"]
            await message.channel.send(random.choice(auswahl))
        else:
            await message.channel.send("😈 Wen soll ich roasten? Mach so: `!roast @Name`")
        return

    if text.startswith("!warn"):
        log_befehl(message.author, "!warn")
        if len(message.mentions) >= 1:
            ziel = message.mentions[0]
            warns[ziel.id] = warns.get(ziel.id, 0) + 1
            await message.channel.send(f"⚠️ {ziel.mention} - Verwarnung von JJ! Das war Warnung Nr. {warns[ziel.id]}! 💅")
        else:
            await message.channel.send("Wen soll ich warnen? Mach so: `!warn @Name`")
        return

    if text == "!regeln":
        log_befehl(message.author, "!regeln")
        await message.channel.send("📜 **Regeln von JJ:**\\n1. Sei lieb! 🤝\\n2. Kein Spam!\\n3. Hab Spaß! 😎\\n4. `hey JJ` wenn du mich brauchst\\n5. 🚫 GRENZE: Nix gegen Familie + keine harten Wörter! Sonst Kick!\\n6. JJ hat immer Recht! 😘")
        return

    if "hey jj" in text or "hey, jj" in text or "heyy jj" in text or "jj bist du da" in text:
        log_befehl(message.author, "hey JJ")
        if modus == "assi":
            antworten = ["Digga, es ist nach 23 Uhr, was willst du von mir? 😂💀 Aber ok, ich bin da...", "Brooo, ich bin im Assi-Modus! Was willst du, du Hodenkobold?! 😂💖", "Jaaa? Ich hab grad gechillt! Was willst du? 😂"]
        elif modus == "frech":
            antworten = ["Jooo! 💅 Da bin ich! Was geht, Digga?", "Heyy! 😎 Die freche JJ ist da!"]
        else:
            antworten = ["Heyyy! 💖 Da bin ich! Hab dich schon vermisst!", "Jaaa Schatz? 😘 Ich bin da!", "Hey! 🥰 Schön, dass du mich rufst!"]
        await message.channel.send(random.choice(antworten))
        return

if __name__ == "__main__":
    Thread(target=run_flask, daemon=True).start()
    token = os.environ.get("DISCORD_TOKEN")
    client.run(token)
