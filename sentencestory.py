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
    model_names = ["llama3.1:8b", "phi3:mini"]
elif API_HOST == "github":
    client = openai.OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=os.getenv("GITHUB_TOKEN")
    )
    model_names = ["meta-llama-3-8b-instruct", "gpt-4o"]
console.print(f"Using {API_HOST} hosted model")


player_colors = ["green", "blue", "red", "yellow", "magenta", "cyan"]
players = ["user"] + model_names
players = model_names
#random.shuffle(players)

current_player_ind = 0


messages = [
        {"role": "system",
        "content":
        """You are playing an Improv game where to goal is to collaboratively write a story together.
        Each round, you will come up with a new sentence to add to the story, and ONLY one sentence.
        If it feels like the story is complete, you can end the game by typing 'The end'.
        Most stories should only be 5-10 sentences long.
        """}
]

while True:
    if messages[-1]["content"].lower().strip(".").endswith("the end"):
        break
    
    current_player = players[current_player_ind]
    current_player_color = "black" if current_player == "user" else player_colors[current_player_ind]
    current_style = Style(color=current_player_color)
    console.print(f"\n[italic]Current player: {current_player}[/italic]", style=current_style)

    if current_player == "user":
        storyline = console.input(f"\nNext sentence: ")
        messages.append({"role": "user", "content": storyline})
    else:
        messages.append({"role": "user", "content": f"Suggest the next sentence in the story, and only one sentence. Your sentence should start with a capital letter and end with a period. Do not say anything after the period."})
        response = client.chat.completions.create(
            model=current_player,
            messages=messages,
            temperature=0.7,
            max_tokens=100
        )
        bot_response = response.choices[0].message.content
        messages.append({"role": "assistant", "content": bot_response})
        console.print(bot_response, style=current_style)
        
    # Switch players
    current_player_ind = (current_player_ind + 1) % len(players)
