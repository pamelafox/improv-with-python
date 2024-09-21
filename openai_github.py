import os

import openai

client = openai.OpenAI(base_url="https://models.inference.ai.azure.com", api_key=os.getenv("GITHUB_TOKEN"))

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are an improv club member playing improv games."},
        {"role": "user", "content": "Suggest a random first line for a scene."},
    ],
)

print("Response:")
print(response.choices[0].message.content)
