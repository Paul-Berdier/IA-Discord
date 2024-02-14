import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Chemin vers le répertoire où se trouve le modèle pré-entraîné
path = "C:/Users/Paul/Documents/Codage/Python/mistral-7B-v0.1"

# Définition du périphérique (GPU ou CPU) sur lequel charger le modèle
device = "cuda" # if torch.cuda.is_available() else "cpu"

# Chargement du modèle et du tokenizer
model = AutoModelForCausalLM.from_pretrained(path).to(device)
tokenizer = AutoTokenizer.from_pretrained(path)

# Définition des messages d'entrée
messages = [
    {"role": "user", "content": "[INST]Do you have mayonnaise recipes?[/INST]"}
]

encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")

generated_ids = model.generate(encodeds.input_ids, max_length=1000, do_sample=True)


decoded = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
print(decoded[0])
