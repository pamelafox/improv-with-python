import os

import azure.identity
import openai
from dotenv import load_dotenv

# Setup the OpenAI client to use either Azure, OpenAI.com, or Ollama API
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST")

if API_HOST == "azure":
    token_provider = azure.identity.get_bearer_token_provider(
        azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    client = openai.AzureOpenAI(
        api_version=os.getenv("AZURE_OPENAI_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_ad_token_provider=token_provider,
    )
    MODEL_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")
elif API_HOST == "ollama":
    client = openai.OpenAI(
        base_url=os.getenv("OLLAMA_ENDPOINT"),
        api_key="nokeyneeded",
    )
    MODEL_NAME = os.getenv("OLLAMA_MODEL")
elif API_HOST == "github":
    client = openai.OpenAI(base_url="https://models.inference.ai.azure.com", api_key=os.getenv("GITHUB_TOKEN"))
    MODEL_NAME = os.getenv("GITHUB_MODEL")
else:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_KEY"))
    MODEL_NAME = os.getenv("OPENAI_MODEL")


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
players = ["user", "meta-llama-3-8b-instruct", "gpt-4o"]
current_player = players[0]

messages = [
        {"role": "system",
        "content":
        """You are playing an Improv game where to goal is to collaboratively write a story together.
        Only complete the sentence once you have been prompted with the start of the sentence.
        """}
]

while True:
    print("\nCurrent player: ", current_player)

    if storyspine_index == len(storyspine):
        print("The story is complete!")
        break

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
