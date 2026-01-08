# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pillow>=12.1.0",
# ]
# ///

import json
import pathlib
from PIL import Image

pathlib.Path("tracker/images/maps").mkdir(parents=True, exist_ok=True)

data = json.load(open("data/celeste.json"))

for chapter in data["chapters"]:
    for side in chapter["sides"]:
        print(chapter["name"], side["name"])

        for checkpoint_idx, checkpoint in enumerate(side["checkpoints"]):
            print("    ", checkpoint["name"])

            id = f"{chapter['id']}_{side['id']}_{checkpoint['abbreviation']}"

            canvas_size = checkpoint["canvas"]["size"]
            canvas_offset = checkpoint["canvas"]["position"]
            image = Image.new("RGBA", (canvas_size["width"], canvas_size["height"]))

            for room_id, room in side["rooms"].items():
                if room["checkpointNo"] != checkpoint_idx:
                    continue
                position = room["canvas"]["position"]
                image.paste(
                    Image.open(
                        f"data/rooms/{chapter['id']}/{side['id']}/{room_id}.png"
                    ),
                    (
                        position["x"] - canvas_offset["x"],
                        position["y"] - canvas_offset["y"],
                    ),
                )

            image.save(f"tracker/images/maps/{id}.png")
