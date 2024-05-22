import os
import subprocess
from random import choice

from tqdm import trange

HOME_FOLDER = ".."
CHARACTERS_FOLDER = os.path.join(HOME_FOLDER, "characters")

SKIP_CHARACTERS = True

characters = {}
for character_name in os.listdir(CHARACTERS_FOLDER):
    modelfile = os.path.join(CHARACTERS_FOLDER, character_name, "Modelfile")
    if not SKIP_CHARACTERS:
        subprocess.run(
            ["ollama", "create", f"-f={modelfile}", character_name], check=True
        )
    characters[character_name] = {}


current_dialog = "capitan (worried): Hello, everyone! You all are well aware of our dire situation\
, so without any let's start the discussion. Does anyone have good ideas?\n"

# TODO: do weighted choice
meta_reactions = [("", 1)]

REPLICA_COUNT = 10

for i in trange(REPLICA_COUNT):
    character_name = choice(list(characters.keys()))
    meta_reaction = choice(meta_reactions)[0]

    ollama_call = subprocess.run(
        ["ollama", "run", character_name, current_dialog + meta_reaction],
        check=True,
        capture_output=True,
    )
    current_dialog += ollama_call.stdout.decode("utf-8")
print(current_dialog)
