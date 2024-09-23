import os

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
console.print(f"Using {API_HOST} hosted model")


player_colors = ["green", "blue", "red", "yellow", "magenta", "cyan"]
players = ["user"] + model_names
# players = model_names
# random.shuffle(players)

current_player_ind = 0


messages = [
    {
        "role": "system",
        "content": """You are playing an Improv game where to goal is to collaboratively write a tweet together.
        Each round, you will come up with a new word to add to the tweet, and ONLY one word.
        DO NOT SUGGEST MORE THAN ONE WORD.
        If it feels like the story is tweet, you can end the tweet by suggesting a hashtag, and ONLY one hashtag.
        A tweet should be no longer than 280 characters.
        """,
    },
    # few shot examples
    {"role": "user", "content": "The"},
    {"role": "assistant", "content": "quick"},
    {"role": "user", "content": "brown"},
    {"role": "assistant", "content": "fox"},
    {"role": "user", "content": "jumps"},
    {"role": "assistant", "content": "over"},
    {"role": "user", "content": "the"},
    {"role": "assistant", "content": "lazy"},
    {"role": "user", "content": "dog"},
    {"role": "assistant", "content": "."},
    {"role": "user", "content": "#AnimalsAreWeird"},
]

tweet_words = []
tweet_so_far = ""

while True:
    if len(tweet_words) > 1 and tweet_words[-1]["word"].lower().strip(".").startswith("#"):
        break

    current_player = players[current_player_ind]
    current_player_color = "black" if current_player == "user" else player_colors[current_player_ind]
    current_style = Style(color=current_player_color)
    console.print(f"\n[italic]Current player: {current_player}[/italic]", style=current_style)

    if current_player == "user":
        word = console.input("\nNext word: ")
        messages.append({"role": "user", "content": word})
    else:
        if tweet_so_far == "":
            messages.append(
                {"role": "user", "content": "Start the tweet by suggesting the first word and ONLY one word."}
            )
        else:
            messages.append(
                {
                    "role": "user",
                    "content": """
                        Suggest the next word in the tweet, and ONLY one word."
                        If the tweet seems over, suggest a hashtag instead.
                        Here is the tweet so far: '{tweet_so_far}'
                        """,
                }
            )
        response = client.chat.completions.create(
            model=current_player, messages=messages, temperature=0.3, max_tokens=5
        )
        bot_response = response.choices[0].message.content
        messages.append({"role": "assistant", "content": bot_response})
        console.print(bot_response, style=current_style)
        word = bot_response

    tweet_words.append({"word": word, "color": current_player_color})
    tweet_so_far += word + " "
    # Switch players
    current_player_ind = (current_player_ind + 1) % len(players)

console.print("\n\nThe final tweet: ")
for word in tweet_words:
    console.print(word["word"], style=Style(color=word["color"]), end=" ")
