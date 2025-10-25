import discord
from discord.ext import tasks, commands
import requests
import os

# Variabile de mediu (setează-le în Railway → Variables)
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

# Intents simple (fără message_content)
intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)

# Ultimul videoclip postat
last_video_id = None

# Funcție care ia cel mai nou videoclip de pe YouTube
def get_latest_video():
    url = (
        f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}"
        f"&channelId={YOUTUBE_CHANNEL_ID}&part=snippet,id&order=date&maxResults=1"
    )
    response = requests.get(url).json()
    items = response.get("items", [])
    if not items:
        return None
    video = items[0]
    video_id = video["id"].get("videoId")
    title = video["snippet"]["title"]
    link = f"https://www.youtube.com/watch?v={video_id}"
    return video_id, title, link

# Task care verifică la fiecare 5 minute pentru videoclipuri noi
@tasks.loop(minutes=5)
async def check_new_video():
    global last_video_id
    latest = get_latest_video()
    if latest is None:
        return

    video_id, title, link = latest
    if last_video_id != video_id:
        last_video_id = video_id
        channel = bot.get_channel(DISCORD_CHANNEL_ID)
        if channel:
            await channel.send(
                f"@everyone 🎬 **P4TEU** a postat un videoclip nou pe YouTube!\n"
                f"👉 **{title}**\n"
                f"📺 Uită-te aici: {link}"
            )

# Când botul pornește
@bot.event
async def on_ready():
    print(f"✅ Botul s-a conectat ca {bot.user}")
    check_new_video.start()  # pornește verificarea automată

bot.run(DISCORD_TOKEN)
