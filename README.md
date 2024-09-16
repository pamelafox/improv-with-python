# Playing improv with Python

This repository contains slides and examples from the PyBay talk "Playing improv with Python".

## Viewing the slides

You can view the slides on GitHub pages for this repo, or by running a local Python server in the repo:

```shell
python -m http.server 8000
```

## Running the examples

If you open this up in a Dev Container or GitHub Codespaces, everything will be setup for you.
If not, follow these steps:

1. Set up a Python virtual environment and activate it.

2. Install the required packages:

    ```bash
    python -m pip install -r requirements.txt
    ```

3. To use GitHub models when running the examples,
    you'll need a `GITHUB_TOKEN` environment variable that stores a GitHub personal access token.
    If you're running this inside a GitHub Codespace, the token will be automatically available.
    If not, generate a new [personal access token](https://github.com/settings/tokens) and run this command to set the `GITHUB_TOKEN` environment variable:

    ```shell
    export GITHUB_TOKEN="<your-github-token-goes-here>"

4. To use Ollama for the examples, you must have Ollama installed and then pull the desired models.

    ```shell
    ollama run llama3.1:8b
    ```

## Available examples

| Example | Description | Suggested Ollama models |
|---------|-------------|---------------------|
| [storyspine.py](storyspine.py) | Generate a story using the Story Spine framework | `llama3.1:8b` |