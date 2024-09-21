import openai

client = openai.OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="nokeyneefsdfeded",
)
model_name = "phi3.5:latest"

response = client.chat.completions.create(
    model=model_name,
    messages=[
        {"role": "system", "content": "You are an improv club member playing improv games."},
        {"role": "user", "content": "Suggest a random first line for a scene."},
    ],
)

print("Response:")
print(response.choices[0].message.content)
