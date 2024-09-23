import json
import os

import openai
from rich.console import Console
from rich.style import Style

console = Console(highlight=False)

# Setup the OpenAI client to use either Ollama or GitHub
API_HOST = "github"

if API_HOST == "github":
    client = openai.OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="nokeyneeded",
    )
    model_names = ["llama3.1:8b"]
elif API_HOST == "github":
    client = openai.OpenAI(base_url="https://models.inference.ai.azure.com", api_key=os.getenv("GITHUB_TOKEN"))
    model_names = ["meta-llama-3-8b-instruct", "gpt-4o"]
console.print(f"Using {API_HOST} hosted model")


player_colors = ["green", "blue", "red", "yellow", "magenta", "cyan"]
players = ["user"] + model_names
# players = model_names
# random.shuffle(players)

current_player_ind = 0


tools = [
    {
        "type": "function",
        "function": {
            "name": "three_things",
            "description": "Suggest an array of three things for the given category. These will get formatted into a comma-separated string.",
            "parameters": {
                "type": "object",
                "properties": {
                    # list of length three
                    "things": {
                        "type": "array",
                        "items": {
                            "type": "string",
                        },
                        "minItems": 3,
                        "maxItems": 3,
                    }
                },
                "additionalProperties": False,
            },
        },
    }
]

messages = [
    {
        "role": "system",
        "content": """You are playing an Improv game where to goal is to suggest lists of three things.
        One player will start off by suggestion the category, like "Three things you bring to Mars",
        and then each player will suggest a list of three things for that category.
        The things don't even have to be real, just suggest whatever comes to mind.
        """,
    },
    {"role": "user", "content": "Three things that you bring to Mars"},
    {"role": "assistant", "tool_calls": [{"id": "call_abc123", "type": "function", "function": {"arguments": '{"things": ["oxygen tank", "spacesuit", "water"]}', "name": "three_things"}}]},
    {"role": "tool", "tool_call_id": "call_abc123", "content": "Oxygen tank, spacesuit, water"},
    {"role": "user", "content": "Food, water, spaceship"},
    {"role": "user", "content": "Suggest three more things that you bring to Mars that are COMPLETELY DIFFERENT from any previous suggestions."},
    {"role": "assistant", "tool_calls": [{"id": "call_abc456", "type": "function", "function": {"arguments": '{"things": ["alien", "laser gun", "teleporter"]}', "name": "three_things"}}]},
    {"role": "tool", "tool_call_id": "call_abc456", "content": "Alien, laser gun, teleporter"},
]

total_turns = len(players) * 2

for current_turn in range(total_turns):
    current_player = players[current_player_ind]
    current_player_color = "black" if current_player == "user" else player_colors[current_player_ind]
    current_style = Style(color=current_player_color)
    console.print(f"\n[italic]Current player: {current_player}[/italic]", style=current_style)

    if current_turn == 0:
        if current_player == "user":
            category = console.input("\nThree things that...")
            messages.append({"role": "user", "content": f"Three things that {category}"})
        else:
            messages.append({"role": "user", "content": "Suggest a category for the three things by finishing the phrase 'Three things that...'"})
            response = client.chat.completions.create(model=current_player, messages=messages, temperature=0.3, max_tokens=30)
            category = response.choices[0].message.content.replace("Three things that", "").replace("Three things", "").strip()
            messages.append({"role": "assistant", "content": f"Three things that {category}"})
            console.print(f"Three things that {category}", style=current_style)
    else:
        if current_player == "user":
            response = console.input(f"\nThree things that {category}: ")
            messages.append({"role": "user", "content": response})
        else:
            messages.append({"role": "user", "content": f"Suggest three more things that {category} that are COMPLETELY DIFFERENT from any previous suggestions."})
            response = client.chat.completions.create(model=current_player, messages=messages, temperature=0.7, max_tokens=100, tools=tools)
            if response.choices[0].message.tool_calls:
                function_args_json = response.choices[0].message.tool_calls[0].function.arguments
                function_args = json.loads(function_args_json)
                if isinstance(function_args.get("things"), list):
                    things_list = function_args.get("things")
                else:
                    things_list = json.loads(function_args.get("things"))
                things = ", ".join(things_list)
            else:
                things = response.choices[0].message.content
            messages.append({"role": "assistant", "content": things})
            console.print(things, style=current_style)

    # Switch players
    current_player_ind = (current_player_ind + 1) % len(players)
