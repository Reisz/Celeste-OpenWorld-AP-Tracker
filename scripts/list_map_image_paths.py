import json

data = json.load(open("data/celeste.json"))

for chapter in data["chapters"]:
    if chapter["id"] == "farewell":
        continue

    for side in chapter["sides"]:
        for checkpoint_idx, checkpoint in enumerate(side["checkpoints"]):
            id = f"{chapter['id']}_{side['id']}_{checkpoint['abbreviation']}"
            print(f"tracker/images/maps/{id}.png")
