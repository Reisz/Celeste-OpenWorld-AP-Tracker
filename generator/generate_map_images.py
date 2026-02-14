# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pillow>=12.1.0",
# ]
# ///

import json
from pathlib import Path
from zipfile import ZipFile

from PIL import Image

OUTPUT_PATH = Path("tracker/images/maps")
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

images = ZipFile("data/berrycamp.zip")
with Path("data/celeste.json").open() as f:
    data = json.load(f)

for chapter in data["chapters"]:
    if chapter["id"] == "farewell":
        continue

    for side in chapter["sides"]:
        print(chapter["name"], side["name"])  # noqa: T201

        for checkpoint_idx, checkpoint in enumerate(side["checkpoints"]):
            print("    ", checkpoint["name"])  # noqa: T201

            canvas_size = checkpoint["canvas"]["size"]
            canvas_offset = checkpoint["canvas"]["position"]
            image = Image.new("RGBA", (canvas_size["width"], canvas_size["height"]))

            for room_id, room in side["rooms"].items():
                if room["checkpointNo"] != checkpoint_idx:
                    continue
                position = room["canvas"]["position"]
                image.paste(
                    Image.open(
                        images.open(
                            f"berrycamp.github.io-dev/public/img/celeste/rooms/{chapter['id']}/{side['id']}/{room_id}.png"
                        )
                    ),
                    (
                        position["x"] - canvas_offset["x"],
                        position["y"] - canvas_offset["y"],
                    ),
                )

            file_name = f"{chapter['id']}_{side['id']}_{checkpoint['abbreviation']}.png"
            image.save(OUTPUT_PATH / file_name)
