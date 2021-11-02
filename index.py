from time import sleep
import os
from youtube_dl import YoutubeDL
import discord
from discord.ext import commands
import random
from dotenv import load_dotenv


ydl_opts = {
    'format' : 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
dotenv_path = ('.env')
load_dotenv(dotenv_path)

client = commands.Bot(command_prefix='-')


@client.command()
async def stop(ctx):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice_client.stop()

@client.command()
async def c(ctx):
    try:
        canal_nome = str(ctx.message.author.voice.channel)
        await ctx.send('ESTOU CONECTADA NO CANAL' +" "+ str(canal_nome))
        connect = discord.utils.get(ctx.guild.voice_channels, name=canal_nome)
        await connect.connect()

        voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
        voice_client.play(discord.FFmpegPCMAudio(executable="vendor/ffmpeg/ffmpeg", source="toca/Bandeirantes.mp3"))
        # voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source="toca/Bandeirantes.mp3"))
    except Exception as e:
        print("#"*100)
        print(e)
        print("#"*100)


@client.command()
async def play(ctx, *, url):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice_client.is_playing():
        await stop(ctx)
    
    await ctx.channel.send("tocando musica")
    songs = os.path.isfile(f"/app/song.mp3")
    
    if songs:
        os.remove('/app/song.mp3')

    ale = random.randint(1, 4)
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice_client.play(discord.FFmpegPCMAudio(executable="vendor/ffmpeg/ffmpeg", source=f"toca/{ale}.mp3"))
    # voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=f"toca\\{ale}.mp3"))
    sleep(2)
    try: 
        if url[:5] == "https":
            with YoutubeDL(ydl_opts) as ydl:
                # url = "ytsearch:"+url
                dados = ydl.extract_info(url, download=False)
                link = dados['formats'][0]['url']
                print(link)
        else:
            with YoutubeDL(ydl_opts) as ydl:
                url = "ytsearch:"+url
                dados = ydl.extract_info(url, download=False)
                p = dados['entries']
                for itens in p:
                    link = itens['url']
                    

        voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice_client.is_playing():
            await stop(ctx)
        
        voice_client.play(discord.FFmpegPCMAudio(link,**FFMPEG_OPTIONS))
    except Exception as e:
        print("#"*100)
        print(e)
        print("#"*100)

@client.command()
async def volume(ctx, volume : int):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice_client.source.volume = volume/100

@client.command()
async def d(ctx):
    try:
        voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice_client.is_playing():
            await stop(ctx)
            voice_client.play(discord.FFmpegPCMAudio(executable="vendor/ffmpeg/ffmpeg", source="toca/palmeiras.mp3"))
            sleep(3)
        else:
            voice_client.play(discord.FFmpegPCMAudio(executable="vendor/ffmpeg/ffmpeg", source="toca/palmeiras.mp3"))
            sleep(3)
        if voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await ctx.send("bot não conectando")
    except Exception as e:
        print("#"*100)
        print(e)
        print("#"*100)

token = os.environ.get("token")
client.run(token)

