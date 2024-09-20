import os

import openai
from rich.console import Console

console = Console(highlight=False)

# Setup the OpenAI client to use either Ollama or GitHub
API_HOST = "ollama"

if API_HOST == "ollama":
    client = openai.OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="nokeyneeded",
    )
    model_name = "phi3.5:latest"
elif API_HOST == "github":
    client = openai.OpenAI(base_url="https://models.inference.ai.azure.com", api_key=os.getenv("GITHUB_TOKEN"))
    model_name = "gpt-4o"

console.print(f"Using {API_HOST} hosted model {model_name}\n")


response = client.chat.completions.create(
    model=model_name,
    messages=[
        {"role": "system", "content": "You are an improv club member playing improv games."},
        {"role": "user", "content": "Suggest a random first line for a scene."},
    ],
)

print("Response:")
print(response.choices[0].message.content)
