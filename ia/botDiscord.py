import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from openai import OpenAI
from gtts import gTTS
import os
import asyncio

# Configuration
TOKEN = "MTE2MzkyMjAzMTA1ODg5NDg5MA.GkDDKs.v9xxZC9uT7Xq9lX-PETKuqIt_5L47FyvbVETXg"
SERVER_IA_URL = "http://localhost:6969/v1"  # URL du serveur IA

# Initialiser le client Discord avec les intentions
intents = discord.Intents.default()
intents.voice_states = True  # Activer les intentions relatives à l'état vocal
intents.messages = True  # Ajoutez les intentions que votre bot utilise
client = commands.Bot(command_prefix='!', intents=intents)

# Initialiser l'assistant OpenAI
openai_client = OpenAI(base_url="http://localhost:6969/v1", api_key="not-needed")

audio_connections = {}

history = [
        {"role": "system",
        "content": "Tu es une intelligence artificiel française. Tu réponds vulgairement aux questions qu'on te pose sans être grossier."}
    ]


def answerIA(question):

    question_history = {
        "role": "user",
        "content": question
    }

    print("L'IA a reçu comme question : " + question)
    history.append(question_history)

    # Obtenir une réponse de l'assistant OpenAI
    completion = openai_client.chat.completions.create(
        model="local-model",
        messages=history,
        temperature=0.7,
        stream=True,
    )

    new_message = {"role": "assistant", "content": ""}

    for chunk in completion:
        if chunk.choices[0].delta.content:
            new_message["content"] += chunk.choices[0].delta.content

    print("L'IA a répondu : " + new_message["content"])
    history.append(new_message)

    return new_message["content"]


@client.event
async def on_ready():
    print('Bot is ready.')


@client.command()
async def ask(ctx, *, question):
    await ctx.send(answerIA(question))


@client.command()
async def askvoc(ctx, *, question):
    # Vérifier si l'auteur de la commande est dans un salon vocal
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        # Rejoindre le salon vocal
        if ctx.guild.id not in audio_connections:
            audio_connections[ctx.guild.id] = await channel.connect()

        # Convertir le texte en audio
        tts_audio = f"tts_{ctx.guild.id}.mp3"
        tts = gTTS(answerIA(question), lang="fr")
        tts.save(tts_audio)

        # Jouer l'audio dans le salon vocal
        audio_connections[ctx.guild.id].play(FFmpegPCMAudio(tts_audio))

        # Attendre la fin de la lecture de l'audio
        while audio_connections[ctx.guild.id].is_playing():
            await asyncio.sleep(1)

        # Supprimer le fichier audio
        os.remove(tts_audio)

    else:
        await ctx.send("You are not in a voice channel.")
        return


# Connecter le bot Discord
client.run(TOKEN)
