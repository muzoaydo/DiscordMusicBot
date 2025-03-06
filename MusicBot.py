import discord
from discord.ext import commands
import yt_dlp
import os

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='-', intents=intents)

ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'cookiefile': 'cookies.txt',
    'quiet': True,
    'extract_flat': 'in_playlist',
    'default_search': 'auto',
    'outtmpl': '%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='join', help='Bot joins the voice channel')
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You are not connected to a voice channel.")

@bot.command(name='leave', help='Bot leaves the voice channel')
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("Bot is not in a voice channel.")

@bot.command(name='play', help='Play a YouTube URL')
async def play(ctx, url: str):
    if not ctx.voice_client:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            return

    async with ctx.typing():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            url2 = info['url']
            title = info.get('title', 'Unknown Title')

        ffmpeg_options = {
            'options': '-vn',
        }

        source = await discord.FFmpegOpusAudio.from_probe(url2, **ffmpeg_options)
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

    await ctx.send(f'Now playing: {title}')

@bot.command(name='pause', help='Pause the current song')
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("Paused the song.")
    else:
        await ctx.send("No song is currently playing.")

@bot.command(name='resume', help='Resume the current song')
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("Resumed the song.")
    else:
        await ctx.send("The song is not paused.")

@bot.command(name='stop', help='Stop the current song')
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Stopped the song.")
    else:
        await ctx.send("No song is currently playing.")

# Bot Token
bot.run(os.getenv('DISCORD_TOKEN'))