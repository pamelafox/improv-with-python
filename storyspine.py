import logging
import os

import openai

logging.basicConfig(level=logging.DEBUG)

# Setup the OpenAI client to use either Ollama or GitHub
API_HOST = "ollama"

if API_HOST == "ollama":
    client = openai.OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="nokeyneeded",
    )
    model_names = ["llama3.1:8b"]
elif API_HOST == "github":
    client = openai.OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=os.getenv("GITHUB_TOKEN")
    )
    model_names = ["meta-llama-3-8b-instruct", "gpt-4o"]
print(f"Using {API_HOST} hosted model")


storyspine = [
    "Once there was… ",
    "And every day… ",
    "Until one day… ",
    "And because of that… ",
    "And because of that… ",
    "And because of that… ",
    "Until finally… ",
    "And so… ",
    "The moral of the story is: "
]
storyspine_index = 0
players = ["user"] + model_names
current_player = players[0]

messages = [
        {"role": "system",
        "content":
        """You are playing an Improv game where to goal is to collaboratively write a story together.
        Only complete the sentence once you have been prompted with the start of the sentence.
        """}
]

while True:
    if storyspine_index == len(storyspine):
        print("The story is complete!")
        break

    print("\nCurrent player: ", current_player)
    next_prompt = storyspine[storyspine_index]
    if current_player == "user":
        storyline = input(f"\n{next_prompt}")
        messages.append({"role": "user", "content": f"{next_prompt} {storyline}"})
    else:
        messages.append({"role": "user", "content": f"Complete the sentence that starts with '{next_prompt}'. Include the full sentence in the response. Only respond with a single sentence."})
        response = client.chat.completions.create(
            model=current_player,
            messages=messages,
            temperature=0.3,
            max_tokens=100
        )
        bot_response = response.choices[0].message.content
        messages.append({"role": "assistant", "content": bot_response})
        print(bot_response)
        
    # Switch players
    storyspine_index += 1
    current_player = players[(players.index(current_player) + 1) % len(players)]
