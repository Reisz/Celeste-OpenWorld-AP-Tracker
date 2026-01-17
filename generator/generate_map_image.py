# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pillow>=12.1.0",
# ]
# ///

import json
import pathlib
import sys
from zipfile import ZipFile

from PIL import Image

pathlib.Path("tracker/images/maps").mkdir(parents=True, exist_ok=True)

images = ZipFile("data/berrycamp.zip")
data = json.load(open("data/celeste.json"))

output_path = pathlib.Path(sys.argv[1])
id = output_path.stem
chapter, side, checkpoint = id.split("_")

chapter = next(x for x in data["chapters"] if x["id"] == chapter)
side = next(x for x in chapter["sides"] if x["id"] == side)
checkpoint_idx, checkpoint = next(
    x for x in enumerate(side["checkpoints"]) if x[1]["abbreviation"] == checkpoint
)

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

image.save(output_path)
