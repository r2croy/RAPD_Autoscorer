import os
import json

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)


def load_json(filepath):
    with open(filepath, "r") as f:
        return json.load(f)
