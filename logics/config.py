
import toml
import os

def load_secrets():
    try:
        with open("secrets.toml", "r") as f:
            return toml.load(f)
    except FileNotFoundError:
        return {}

SECRETS = load_secrets()
