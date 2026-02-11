import json
from pathlib import Path

with Path("data/celeste.json").open() as f:
    data = json.load(f)

for chapter in data["chapters"]:
    if chapter["id"] == "farewell":
        continue

    for side in chapter["sides"]:
        for checkpoint in side["checkpoints"]:
            name = f"{chapter['id']}_{side['id']}_{checkpoint['abbreviation']}"
            print(f"tracker/images/maps/{name}.png")  # noqa: T201
