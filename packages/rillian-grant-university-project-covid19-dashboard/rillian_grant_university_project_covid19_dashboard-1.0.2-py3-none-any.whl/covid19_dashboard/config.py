"""Loads config.json"""

import json

try:
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
except FileNotFoundError:
    config = {
        "newsapi_key": "31c1a215c63d49fa9c3a65d259934575",
        "logging": {
            "file": ""
        },
        "location": "Exeter",
        "location-type": "ltla",
        "location-nation": "England",
        "flask_debug": False,
        "host": "0.0.0.0",
        "port": 80
    }
