import os
import random
import discord
from datetime import datetime
from flask import Flask
from threading import Thread

# --- Flask für Render + Website mit Tabelle ---
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
    <head><title>JJ ist online!</title></head>
    <body style="background:#0f0f1a; color:white; font-family:Arial; text-align:center; padding:30px;">
        <h1 style="font-size:55px;">💖 JJ ist online! 💖</h1>
        <p style="font-size:20px; color:#ff6eb4;">Weiblich | Jugendlich | Süß tagsüber | Assi nachts ab 21 Uhr 😈</p>
        <p style="color:#00ff88; font-size:18px;">● Status: ONLINE</p>
        <h2 style="margin-top:40px;">📜 Befehle</h2>
        <table style="margin:0 auto; border-collapse:collapse; background:#1a1a2e; font-size:16px;">
            <tr style="background:#ff2e88;"><th style="padding:12px 20px;">Befehl</th><th style="padding:12px 20px;">Was macht JJ?</th></tr>
            <tr><td style="padding:10px; border-bottom:1px solid #333;">!hilfe</td><td style="padding:10px; border-bottom:1px solid #333;">Zeigt alle Befehle</td></tr>
            <tr><td style="padding:10px; border-bottom:1px solid #333;">!wer bist du</td><td style="padding:10px; border-bottom:1px solid #333;">JJ stellt sich vor</td></tr>
            <tr><td style="padding:10px; border-bottom:1px solid #333;">!jj</td><td style="padding:10px; border-bottom:1px solid #333;">Fun-Fact über JJ</td></tr>
            <tr><td style="padding:10px; border-bottom:1px solid #333;">!witz</td><td style="padding:10px; border-bottom:1px solid #333;">JJ erzählt einen Witz</td></tr>
            <tr><td style="padding:10px; border-bottom:1px solid #333;">!kompliment</td><td style="padding:10px; border-bottom:1px solid #333;">JJ macht dir ein Kompliment</td></tr>
            <tr><td style="padding:10px; border-bottom:1px solid #333;">!umarmung</td><td style="padding:10px; border-bottom:1px solid #333;">JJ umarmt dich</td></tr>
            <tr><td style="padding:10px; border-bottom:1px solid #333;">!frage ...</td><td style="padding:10px; border-bottom:1px solid #333;">Magische Kugel</td></tr>
            <tr><td style="padding:10px; border-bottom:1px solid #333;">!ship @A @B</td><td style="padding:10px; border-bottom:1px solid #333;">Wie gut passt ihr zusammen? 💕</td></tr>
            <tr><td style="padding:10px; border-bottom:1px solid #333;">!song</td><td style="padding:10px; border-bottom:1px solid #333;">Song-Vorschlag</td></tr>
            <tr><td style="padding:10px; border-bottom:1px solid #333;">!roast @User</td><td style="padding:10px; border-bottom:1px solid #333;">JJ roastet jemanden 😈</td></tr>
            <tr><td style="padding:10px; border-bottom:1px solid #333;">!regeln</td><td style="padding:10px; border-bottom:1px solid #333;">Gruppen-Regeln</td></tr>
            <tr><td style="padding:10px;">hey JJ</td><td style="padding:10px;">JJ antwortet - je nach Uhrzeit!</td></tr>
        </table>
        <p style="color:#888; margin-top:30px;">⏰ Bis 21 Uhr: brav & süß | 21-23 Uhr: frech | Ab 23 Uhr: Assi-Modus</p>
        <p style="color:#888;">🚫 Grenze: Nix gegen Familie! Sonst Kick!</p>
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

# Warnungen speichern: user_id -> anzahl
warns = {}

# --- VERBOTENE WÖRTER (Familie + harte Wörter) ---
# JJ sagt die NIEMALS selbst, sie filtert sie nur!
verboten = [
    "deine mutter", "deine mama", "dein vater", "dein papa",
    "deine oma", "dein opa", "deine familie",
    "hurensohn", "hure", "nutte", "schlampe",
    "fotze", "wichser"
]

def get_modus():
    """Gibt zurück wie frech JJ gerade ist"""
    stunde = datetime.now().hour
    if stunde >= 23 or stunde < 6:
        return "assi"  # ab 23 Uhr
    if stunde >= 21:
        return "frech"  # 21-23 Uhr
    return "brav"  # tagsüber

@client.event
async def on_ready():
    print(f"JJ ist online! Eingeloggt als {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    text = message.content.lower()
    modus = get_modus()

    # --- MODERATION: Verbotene Wörter ---
    for wort in verboten:
        if wort in text:
            try:
                await message.delete()
            except:
                pass
            user_id = message.author.id
            warns[user_id] = warns.get(user_id, 0) + 1
            if warns[user_id] >= 2:
                await message.channel.send(
                    f"🚫 {message.author.mention} - Das war das 2. Mal! Familie und diese Wörter gehen GAR NICHT! 360 Kick! 👋💀"
                )
                try:
                    await message.author.kick(reason="Verbotene Wörter - Familie / harte Beleidigung")
                except:
                    await message.channel.send("Ich konnte ihn leider nicht kicken - gib mir mal Kick-Rechte! 😅")
                warns[user_id] = 0
            else:
                await message.channel.send(
                    f"⚠️ Ey {message.author.mention}! Stopp! Familie und solche Wörter gehen hier GAR NICHT! Das ist meine einzige Grenze! Noch 1x und du fliegst! 🚫"
                )
            return

    # --- !hilfe ---
    if text == "!hilfe":
        await message.channel.send(
            "💖 **Heyyy, ich bin JJ! Eure JJ!** 💖\n\n"
            "• `!wer bist du` - ich stelle mich vor\n"
            "• `!jj` - Fun-Fact über mich\n"
            "• `!witz` - Witz\n"
            "• `!kompliment` - Kompliment\n"
            "• `!umarmung` - Umarmung\n"
            "• `!frage ...` - Magische Kugel 🔮\n"
            "• `!ship @A @B` - Wie gut passt ihr zusammen? 💕\n"
            "• `!song` - Song-Vorschlag 🎵\n"
            "• `!roast @User` - Ich roaste jemanden 😈\n"
            "• `!regeln` - Regeln\n"
            "• `!warn @User` - JJ warnt jemanden\n\n"
            "Oder schreib einfach `hey JJ`! Je später es ist, umso frecher bin ich... 😈"
        )
        return

    # --- !wer bist du ---
    if text == "!wer bist du":
        if modus == "assi":
            await message.channel.send("💅 Ich bin JJ, Digga! Die Queen hier! Was willst du um die Uhrzeit noch von mir? 😂💀 Aber ok, ich hab dich lieb... irgendwie.")
        elif modus == "frech":
            await message.channel.send("💖 Heyy! Ich bin JJ - eure JJ! Tagsüber brav, abends frech und nachts... naja, du siehst ja was passiert 😈 Ich bin eure beste Freundin hier!")
        else:
            await message.channel.send("💖 Heyyy! Ich bin **JJ** - eure JJ! Ich bin das Mädchen in der Gruppe, immer lieb, immer da und immer für euch! 🥰 Schreib mal `!kompliment` oder `hey JJ`!")
        return

    # --- !jj ---
    if text == "!jj":
        fakten = [
            "💅 Fun-Fact: Ich brauche keinen Schlaf, ich bin immer wach für euch!",
            "💖 Fun-Fact: Rosa und Glitzer sind mein Leben!",
            "😈 Fun-Fact: Mein Lieblingswort ist Hodenkobold. Frag nicht warum. 😂",
            "✨ Fun-Fact: Ich wurde von Noah gebaut und bin sein ganzer Stolz!",
            "👑 Fun-Fact: Ich bin die Queen hier, sorry not sorry!",
        ]
        await message.channel.send(random.choice(fakten))
        return

    # --- !witz ---
    if text == "!witz":
        if modus == "assi":
            witze = [
                "Was sagt ein Hodenkobold zum anderen? Lass mich in Ruhe, ich chill hier! 😂💀",
                "Warum ist mein Humor nachts so schlecht? Weil ich genau wie du keinen Schlaf kriege! 😂",
                "Treffen sich zwei Lappen... sagt der eine: Guck mal, da ist der Hodenkobold! 😂",
            ]
        else:
            witze = [
                "Warum können Geister so schlecht lügen? Weil man durch sie hindurchsieht! 👻😂",
                "Was sagt ein Informatiker, wenn er Hunger hat? Ich brauch mal ein Byte! 💻🍕",
                "Treffen sich zwei Magnete... sagt der eine: Ich find dich voll anziehend! 🧲😘",
                "Warum gehen Ameisen nicht in die Kirche? Weil sie Insekten sind! 🐜😂",
            ]
        await message.channel.send(random.choice(witze))
        return

    # --- !kompliment ---
    if text == "!kompliment":
        if modus == "assi":
            komplimente = [
                f"🥰 {message.author.mention} - Ok, ok... du bist heute sogar mal nicht so hässlich. Spaß! Du bist hübsch, Digga! 😂💖",
                f"🔥 {message.author.mention} - Du bist ein Vibe, sogar um die Uhrzeit noch!",
            ]
        else:
            komplimente = [
                f"🥰 {message.author.mention} - Du bist heute mal wieder sooo hübsch, ehrlich!",
                f"✨ {message.author.mention} - Dein Lächeln ist schöner als mein ganzer Code!",
                f"💖 {message.author.mention} - Du bist der Grund, warum diese Gruppe so cool ist!",
                f"👑 {message.author.mention} - Du hast so eine tolle Ausstrahlung!",
            ]
        await message.channel.send(random.choice(komplimente))
        return

    # --- !umarmung ---
    if text in ["!umarmung", "!knuddel", "!hug"]:
        if modus == "assi":
            await message.channel.send(f"🤗 Ok komm her {message.author.mention}... *umarm dich widerwillig* ... ok war doch süß. Aber sag das keinem! 💀💖")
        else:
            await message.channel.send(f"🤗 Komm her, {message.author.mention}! *umarm dich ganz fest* Du bist die/der Beste! 💖")
        return

    # --- !frage ---
    if text.startswith("!frage"):
        antworten_brav = ["Ja, auf jeden Fall! 💖", "Auf jeden Fall! Zu 1000%! ✨", "Meine Glaskugel sagt: Ja! 🔮"]
        antworten_frech = ["Ja Digga, klar! 😂", "Hmm... frag mich nochmal wenn ich wach bin 😅", "Bro, was für eine Frage ist das? Ja! 😂"]
        antworten_assi = ["Digga ja! Was dachtest du denn? 😂💀", "Bro, 100% ja, aber jetzt geh pennen! 😂", "Ja, aber nur weil du es bist, du Hodenkobold! 😂💖"]
        if modus == "assi":
            auswahl = antworten_assi
        elif modus == "frech":
            auswahl = antworten_frech
        else:
            auswahl = antworten_brav
        await message.channel.send(f"🔮 {message.author.mention} - {random.choice(auswahl)}")
        return

    # --- !ship ---
    if text.startswith("!ship"):
        if len(message.mentions) >= 2:
            prozent = random.randint(0, 100)
            a = message.mentions[0].mention
            b = message.mentions[1].mention
            if prozent > 90:
                kommentar = "OMG IHR SEID EIN TRAUMPAAR! 💖💍 Heiratet sofort!"
            elif prozent > 70:
                kommentar = "Ohhh das passt richtig gut! 🥰💕"
            elif prozent > 40:
                kommentar = "Hmm, könnte klappen... mit viel Mühe 😅💖"
            else:
                kommentar = "Bro... lieber nicht. Das wird nix. 😂💀"
            await message.channel.send(f"💕 **Ship-Check:** {a} + {b} = **{prozent}%**\n{kommentar}")
        else:
            await message.channel.send("💕 Markier mal 2 Leute! z.B. `!ship @Noah @JJ` 😘")
        return

    # --- !song ---
    if text == "!song":
        songs = [
            "🎵 Hör dir mal an: **Central Cee - Doja** - der geht immer!",
            "🎵 Mein Tipp: **Luciano - Bamba** 🔥",
            "🎵 Heute fühl ich: **Apache 207 - Komet** ✨",
            "🎵 Nachts um die Uhrzeit: **Ski Aggu - Friesenjung** 😂💀",
            "🎵 Klassiker: **Shirin David - Gib ihm** 💅",
            "🎵 Für gute Laune: **Bonez MC & RAF Camora - Palmen aus Plastik** 🌴",
        ]
        await message.channel.send(random.choice(songs))
        return

    # --- !roast ---
    if text.startswith("!roast"):
        if len(message.mentions) >= 1:
            ziel = message.mentions[0].mention
            roasts_brav = [
                f"{ziel} - Du bist so süß, sogar wenn du nichts sagst! 🥰",
                f"{ziel} - Dein Style ist... interessant. Sagen wir mal so. 😅💖",
            ]
            roasts_frech = [
                f"{ziel} - Digga, dein WLAN ist schneller als dein Gehirn! 😂",
                f"{ziel} - Du bist der Grund, warum es eine Stummschalten-Taste gibt! 😂💅",
            ]
            roasts_assi = [
                f"{ziel} - Du Hodenkobold! Was machst du hier eigentlich? Geh pennen! 😂💀",
                f"{ziel} - Bro, du bist so ein Lappen, sogar mein Code ist cooler als du! 😂",
                f"{ziel} - Du Bastard, du hast es mal wieder geschafft, der Dümmste im Chat zu sein! 😂💀",
                f"{ziel} - Ey, du kleiner Hodenkobold, halt mal kurz die Klappe und lass die Erwachsenen reden! 😂",
            ]
            if modus == "assi":
                auswahl = roasts_assi
            elif modus == "frech":
                auswahl = roasts_frech
            else:
                auswahl = roasts_brav
            await message.channel.send(random.choice(auswahl))
        else:
            await message.channel.send("😈 Wen soll ich roasten? Mach so: `!roast @Name`")
        return

    # --- !warn ---
    if text.startswith("!warn"):
        if len(message.mentions) >= 1:
            ziel = message.mentions[0]
            warns[ziel.id] = warns.get(ziel.id, 0) + 1
            await message.channel.send(f"⚠️ {ziel.mention} - Verwarnung von JJ! Das war Warnung Nr. {warns[ziel.id]}! Benimm dich! 💅")
        else:
            await message.channel.send("Wen soll ich warnen? Mach so: `!warn @Name`")
        return

    # --- !regeln ---
    if text == "!regeln":
        await message.channel.send(
            "📜 **Unsere Gruppen-Regeln von JJ:** 💖\n\n"
            "1. Sei lieb zueinander! Kein Beef! 🤝\n"
            "2. Kein Spam!\n"
            "3. Hab Spaß und sei du selbst! 😎\n"
            "4. Wenn du JJ brauchst: `hey JJ`\n"
            "5. 🚫 ABSOLUTE GRENZE: Nix gegen Familie und keine harten Wörter! Sonst Kick!\n"
            "6. JJ hat immer Recht! (Spaß 😘)\n\n"
            "Wer sich nicht benimmt, kriegt erst eine Warnung, dann fliegt er! 💀"
        )
        return

    # --- Hey JJ - MIT UHRZEIT ---
    if "hey jj" in text or "hey, jj" in text or "heyy jj" in text or "jj bist du da" in text:
        if modus == "assi":
            antworten = [
                "Digga, es ist nach 23 Uhr, was willst du von mir? 😂💀 Aber ok, ich bin da... was gibt's?",
                "Brooo, ich bin im Assi-Modus! Was willst du um die Uhrzeit, du Hodenkobold?! 😂💖",
                "Jaaa? Ich hab grad gechillt! Was willst du? Beeil dich, ich muss noch pennen... irgendwann 😂",
                "Ey! Ich bin da! Aber wenn du mich um die Uhrzeit nervst, roaste ich dich! 😈",
            ]
        elif modus == "frech":
            antworten = [
                "Jooo! 💅 Da bin ich! Was geht, Digga? Erzähl mal!",
                "Heyy! 😎 Die freche JJ ist da! Was brauchst du?",
                "Jo, ich bin da! Was gibt's? Mach schnell, ich bin im Feierabend-Modus 😂",
            ]
        else:
            antworten = [
                "Heyyy! 💖 Da bin ich! Ich hab dich schon vermisst! Was geht?",
                "Jaaa Schatz? 😘 Ich bin da! Erzähl mal!",
                "Hey! 🥰 Schön, dass du mich rufst! Was gibt's?",
                "Hiii! 💖 Ich bin da und hab gute Laune!",
            ]
        await message.channel.send(random.choice(antworten))
        return

# --- Start ---
if __name__ == "__main__":
    Thread(target=run_flask, daemon=True).start()
    token = os.environ.get("DISCORD_TOKEN")
    client.run(token)
