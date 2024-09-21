import base64
import os

import ollama
import openai
from rich.console import Console
from rich.style import Style

console = Console(highlight=False)

# Setup the OpenAI client to use either Ollama or GitHub
API_HOST = "ollama"

if API_HOST == "ollama":
    client = openai.OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="nokeyneeded",
    )
    model_names = ["llama3.1:8b", "phi3.5:latest"]
elif API_HOST == "github":
    client = openai.OpenAI(base_url="https://models.inference.ai.azure.com", api_key=os.getenv("GITHUB_TOKEN"))
    model_names = ["meta-llama-3-8b-instruct", "gpt-4o"]
console.print(f"Using {API_HOST} hosted model\n")


player_colors = ["green", "blue", "red", "yellow", "magenta", "cyan"]
players = ["user"] + model_names
# players = model_names
# random.shuffle(players)

current_player_ind = 0
num_rounds = 5

messages = [
    {
        "role": "system",
        "content": """You are playing an Improv game with the goal of collaboratively describing a new product together.
    Each round, you will come up with a new sentence describing the product, starting with 'Yes, and...'.
    At the end, you will come up with a great name or the product.
    """,
    },
    # Few shot examples
    {"role": "user", "content": "Introducing our brand new product, a ball that shoots laser beams!"},
    {"role": "assistant", "content": "Yes, and it also has a built-in camera."},
    {"role": "user", "content": "Yes, and it can fly."},
    {"role": "assistant", "content": "Yes, and it can also be controlled with your mind."},
]

# Get the first line of the product description


def open_image_as_base64(filename):
    with open(filename, "rb") as image_file:
        image_data = image_file.read()
    image_base64 = base64.b64encode(image_data).decode("utf-8")
    return f"data:image/png;base64,{image_base64}"


PROP_IMAGE = "images/toy_sonicscrewdriver.png"
PROP_PROMPT = """
"Pretend you've NEVER EVER seen this object before,
and describe it as if it is a new invention from a toy company.
Use only a single sentence to describe it. Do not name it."
"""
if API_HOST == "ollama":
    response = ollama.chat(model="llava", messages=[{"role": "user", "content": PROP_PROMPT, "images": [PROP_IMAGE]}])
    product_description = response["message"]["content"]
else:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "assistant", "content": "Introducing our brand new product, a ball that shoots laser beams!"},
            {
                "role": "user",
                "content": [
                    {"text": PROP_PROMPT, "type": "text"},
                    {
                        "image_url": {"url": open_image_as_base64(PROP_IMAGE)},
                        "type": "image_url",
                    },
                ],
            },
        ],
        temperature=0.7,
    )
    product_description = response.choices[0].message.content

messages.append({"role": "user", "content": product_description})
console.print(f"What are we building? \n {product_description}")

for current_round in range(num_rounds):
    current_player = players[current_player_ind]
    current_player_color = "black" if current_player == "user" else player_colors[current_player_ind]
    current_style = Style(color=current_player_color)
    console.print(f"\n[italic]Current player: {current_player}[/italic]", style=current_style)

    if current_round == num_rounds - 1:
        if current_player == "user":
            product_name = console.input("\nWhat is the name of this product? Be inventive! ")
        else:
            messages.append(
                {
                    "role": "user",
                    "content": (
                        "What is the name of this product? Be inventive!"
                        "ONLY respond with the name, not the reasoning or anything else."
                    ),
                }
            )
            response = client.chat.completions.create(
                model=model_names[0], messages=messages, temperature=0.7, max_tokens=20
            )
            product_name = response.choices[0].message.content
        console.print(f"\n[bold]Product name: {product_name}[/bold]", style=current_style)
        break

    if current_player == "user":
        storyline = console.input("\nYour description: ")
        messages.append({"role": "user", "content": storyline})
    else:
        if current_round == num_rounds - 1:
            messages.append({"role": "user", "content": "What is the name of this product? Be inventive!"})
        response = client.chat.completions.create(
            model=current_player, messages=messages, temperature=0.7, max_tokens=100
        )
        bot_response = response.choices[0].message.content
        messages.append({"role": "assistant", "content": bot_response})
        console.print(bot_response, style=current_style)

    # Switch players
    current_player_ind = (current_player_ind + 1) % len(players)
