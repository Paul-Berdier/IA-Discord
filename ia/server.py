from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Initialiser l'assistant intelligent
client = OpenAI(base_url="http://localhost:6969/v1", api_key="not-needed")

# Historique initial de la conversation
history = [
    {"role": "system",
     "content": "Tu es une intelligence artificiel française. Tu réponds avec VULGARITé aux questions qu'on te pose sans être obligé d'y répondre correctement."},
    {"role": "user",
     "content": "Bonjour, présente-toi."},
]


@app.route('/', methods=['POST'])
def chat_with_assistant():
    data = request.json
    question = data.get('question')

    # Obtenir une réponse de l'assistant intelligent
    completion = client.chat.completions.create(
        model="local-model",
        messages=history + [{"role": "user", "content": question}],
        temperature=0.7,
        stream=True,
    )

    new_message = {"role": "assistant", "content": ""}

    for chunk in completion:
        if chunk.choices[0].delta.content:
            new_message["content"] += chunk.choices[0].delta.content

    history.append({"role": "user", "content": question})
    history.append(new_message)

    # Renvoyer la réponse au format JSON
    return jsonify({"answer": new_message["content"]})


if __name__ == '__main__':
    app.run(port=3003)  # Changez le port si nécessaire

    history.append(new_message)

    # Uncomment to see chat history
    # import json
    # gray_color = "\033[90m"
    # reset_color = "\033[0m"
    # print(f"{gray_color}\n{'-'*20} History dump {'-'*20}\n")
    # print(json.dumps(history, indent=2))
    # print(f"\n{'-'*55}\n{reset_color}")

    print()
    history.append({"role": "user", "content": input("> ")})