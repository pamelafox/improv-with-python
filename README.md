# Playing improv with Python

This repository contains slides and games from the PyBay talk "Playing improv with Python".

* [Viewing the slides](#viewing-the-slides)
* [Running the games](#running-the-games)
* [Available games](#available-games)

## Viewing the slides

You can view the slides [published on GitHub pages](https://pamelafox.github.io/improv-with-python/), or by running a local Python server in the repo:

```shell
python -m http.server 8000
```

## Running the games

If you open this up in a VS Code Dev Container or GitHub Codespaces, everything will be setup for you.
If not, follow these steps:

1. Set up a Python virtual environment and activate it.

2. Install the required packages:

    ```bash
    python -m pip install -r requirements.txt
    ```

3. To use GitHub models for the games,
    you'll need a `GITHUB_TOKEN` environment variable that stores a GitHub personal access token.
    If you're running this inside a GitHub Codespace, the token will be automatically available.
    If not, generate a new [personal access token](https://github.com/settings/tokens) and run this command to set the `GITHUB_TOKEN` environment variable:

    ```shell
    export GITHUB_TOKEN="your-github-token-goes-here"

4. To use Ollama for the games, you must have Ollama installed and then pull any models required for each game.

    ```shell
    ollama run llama3.1:8b
    ```

## Available games

| Improv game | Python code | Notable features |
|-------------|-------------|------------------|
| [Story Spine](https://github.com/pamelafox/improvlists/blob/master/games/Game%3A-Group-Story-Spine.md) | [storyspine.py](storyspine.py) | Each response must start with a specific string |
| [Sentence-at-a-time](https://github.com/pamelafox/improvlists/blob/master/games/Game%3A-Sentence-at-a-time-Story.md) | [sentencestory.py](sentencestory.py) | Specifies a phrase to end the story |
| [Tweet generator](https://github.com/pamelafox/improvlists/blob/master/games/Game%3A-Tweet-Generator.md) | [tweetgenerator.py](tweetgenerator.py) | Uses few-shot prompting to encourage model to return single word |
| [Yes, And Product Factory](https://github.com/pamelafox/improvlists/blob/master/games/Game%3A-Yes%2C-And...-Product-Factory.md) | [yesandproduct.py](yesandproduct.py) | Uses vision models (llava/gpt-4o) to describe prop |
| [Three Things!](https://github.com/pamelafox/improvlists/blob/master/games/Game%3A-3-Things!.md) | [threethings_simple.py](threethings_simple.py) | Starts with a different prompt than subsequent rounds. |
| [Three Things!](https://github.com/pamelafox/improvlists/blob/master/games/Game%3A-3-Things!.md) | [threethings_tools.py](threethings_tools.py) | Same, but uses function calling and few shots to force a list of 3 strings. |
