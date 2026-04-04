# EVA Virtual Assistant - ADVANCED
Welcome to the EVA (Advanced) Virtual Assistant Project!

## Introduction
EVA is an advanced virtual assistant (as seen by the name) that allows the user to execute various tasks on their device with precision and power. It can handle complex tasks, queries and answer difficult questions, while being able to reason and talk with the user normally as if it was a friendly companion!

## How to use EVA?
Using EVA is pretty simple, especially if you have a Mac! Just follow the following steps:
- First, download the source code onto your device and open it in a code editor.
- Then, create a new python virtual environment using `python3 -m venv .venv`
- Next, activate your python venv by doing `source .venv/bin/activate`
- You will need to install the required and recommended python libraries. To do this, you can run `pip install -r requirements.txt` and all necessary libraries will be installed. Please note that this may take some time.
- Setup is almost complete! You will be needing a Piper model, which you can get here: https://huggingface.co/rhasspy/piper-voices/tree/main (make sure to download both the .onnx and the .onnx.json file for that model)
- Place your .onnx and .onnx.json files inside the models/voice_models folder. Don't forget to change the path to Piper in `core/functions/speech` as well!
- Finally, you will be needing an Ollama model to run this. You can download Ollama at https://ollama.com/download.
- You can install the default Ollama model used here by doing `ollama pull qwen3:4b-q4_K_M`
And thats it! Just run the `main.py` file using `python -m main` and watch EVA run!
> NOTE: First few runs do tend to take some time. LLM will get faster as the model warms up. Same goes for Piper.

### More Information will be out soon!
Official Docs: https://eva-virtual-assistant.notion.site/EVA-AI-337d6094011980ec89fed83db235bb4c
> Happy coding! - LC
