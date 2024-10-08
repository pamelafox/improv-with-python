import os
import random

import openai
from rich import print
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
console.print(f"Using {API_HOST} hosted model")


storyspine = [
    "Once there was… ",
    "And every day… ",
    "Until one day… ",
    "And because of that… ",
    "And because of that… ",
    "And because of that… ",
    "Until finally… ",
    "And so… ",
    "The moral of the story is: ",
]

player_colors = ["green", "blue", "red", "yellow", "magenta", "cyan"]
players = ["user"] + model_names
# players = model_names
random.shuffle(players)

current_player_ind = 0
storyspine_index = 0


messages = [
    {
        "role": "system",
        "content": """You are playing an Improv game where to goal is to collaboratively write a story together.
        Only complete the sentence once you have been prompted with the start of the sentence.
        """,
    }
]

while True:
    if storyspine_index == len(storyspine):
        print("The story is complete!")
        break

    current_player = players[current_player_ind]
    current_player_color = "black" if current_player == "user" else player_colors[current_player_ind]
    current_style = Style(color=current_player_color)

    console.print(f"\n[italic]Current player: {current_player}[/italic]", style=current_style)
    next_prompt = storyspine[storyspine_index]
    if current_player == "user":
        storyline = console.input(f"\n{next_prompt}")
        messages.append({"role": "user", "content": f"{next_prompt} {storyline}"})
    else:
        messages.append(
            {
                "role": "user",
                "content": f"Complete the sentence that starts with '{next_prompt}'. Include the full sentence in the response. Only respond with a single sentence.",
            }
        )
        response = client.chat.completions.create(model=current_player, messages=messages, temperature=0.7, max_tokens=100)
        bot_response = response.choices[0].message.content
        messages.append({"role": "assistant", "content": bot_response})
        console.print(bot_response, style=current_style)

    # Switch players
    storyspine_index += 1
    current_player_ind = (current_player_ind + 1) % len(players)
