import json
import multiprocessing
from dataclasses import dataclass
from pathlib import Path
from zipfile import ZipFile

from PIL import Image

OUTPUT_PATH = Path("tracker/images/maps")
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

with Path("data/celeste.json").open() as f:
    data = json.load(f)


@dataclass
class Room:
    zip_path: str
    x: int
    y: int


@dataclass
class Map:
    width: int
    height: int
    rooms: list[Room]
    output_path: Path


def build_map_image(map_data: Map) -> None:
    images = ZipFile("data/berrycamp.zip")
    image = Image.new("RGBA", (map_data.width, map_data.height))

    for room in map_data.rooms:
        image.paste(Image.open(images.open(room.zip_path)), (room.x, room.y))

    image.save(map_data.output_path)


if __name__ == "__main__":
    maps = []
    for chapter in data["chapters"]:
        if chapter["id"] == "farewell":
            continue

        for side in chapter["sides"]:
            for checkpoint_idx, checkpoint in enumerate(side["checkpoints"]):
                canvas_size = checkpoint["canvas"]["size"]
                canvas_offset = checkpoint["canvas"]["position"]

                rooms = []
                for room_id, room in side["rooms"].items():
                    if room["checkpointNo"] != checkpoint_idx:
                        continue
                    position = room["canvas"]["position"]
                    rooms.append(
                        Room(
                            f"berrycamp.github.io-dev/public/img/celeste/rooms/{chapter['id']}/{side['id']}/{room_id}.png",
                            position["x"] - canvas_offset["x"],
                            position["y"] - canvas_offset["y"],
                        )
                    )

                file_name = (
                    f"{chapter['id']}_{side['id']}_{checkpoint['abbreviation']}.png"
                )
                maps.append(
                    Map(
                        canvas_size["width"],
                        canvas_size["height"],
                        rooms,
                        OUTPUT_PATH / file_name,
                    )
                )

    with multiprocessing.Pool() as pool:
        pool.map(build_map_image, maps)
