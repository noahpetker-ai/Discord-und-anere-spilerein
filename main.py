import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"JJ is online!")
    def log_message(self, *args):
        pass

def run_server():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(('0.0.0.0', port), Handler).serve_forever()

threading.Thread(target=run_server, daemon=True).start()

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"JJ ist online als {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! JJ ist da! 🏓")

@bot.command()
async def moin(ctx):
    await ctx.send(f"Moin {ctx.author.mention}!")

bot.run(os.environ.get("DISCORD_TOKEN"))
