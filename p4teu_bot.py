import discord
from discord.ext import tasks, commands
import requests
import os

# variabile de mediu
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

# intents corect configurate
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Comandă de test
@bot.command()
async def test(ctx):
    await ctx.send("@everyone 🎬 **P4TEU** a postat un videoclip nou pe YouTube!\n👉 **Titlul Test**\n📺 Uită-te aici: https://www.youtube.com/watch?v=dQw4w9WgXcQ")

@bot.event
async def on_ready():
    print(f"✅ Botul s-a conectat ca {bot.user}")

bot.run(DISCORD_TOKEN)
