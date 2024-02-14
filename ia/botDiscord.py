import discord
from discord.ext import commands
from openai import OpenAI

# Configuration
TOKEN = "MTE2MzkyMjAzMTA1ODg5NDg5MA.GkDDKs.v9xxZC9uT7Xq9lX-PETKuqIt_5L47FyvbVETXg"
SERVER_IA_URL = "http://localhost:6969/v1"  # URL du serveur IA

# Initialiser le client Discord avec les intentions
intents = discord.Intents.default()
intents.messages = True  # Ajoutez les intentions que votre bot utilise
client = commands.Bot(command_prefix='!', intents=intents)

# Initialiser l'assistant OpenAI
openai_client = OpenAI(base_url="http://localhost:6969/v1", api_key="not-needed")

history = [
        {"role": "system",
        "content": "Tu es une intelligence artificiel française. Tu réponds vulgairement aux questions qu'on te pose sans être grossier."}
    ]

@client.event
async def on_ready():
    print('Bot is ready.')


@client.command()
async def ask(ctx, *, question):

    question_history = {"role": "user",
        "content": question}

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

    await ctx.send(new_message["content"])
    history.append(new_message)
    print("L'IA a répondu : " + new_message["content"])


# Connecter le bot Discord
client.run(TOKEN)
