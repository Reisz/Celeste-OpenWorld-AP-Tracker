"""Generates map images from Berrycamp data and room images."""

import json
import multiprocessing
from dataclasses import dataclass
from pathlib import Path
from zipfile import ZipFile

from lib.iterators import iterate_checkpoints, iterate_rooms
from PIL import Image

MAX_IMAGE_DIMENSIONS = 4096

OUTPUT_PATH = Path("tracker/images/maps")
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

with Path("data/celeste.json").open() as f:
    data = json.load(f)


@dataclass
class Room:
    """Berrycamp room image path and position within the final map."""

    zip_path: str
    x: int
    y: int


@dataclass
class Map:
    """Map image to be built."""

    size: tuple[int, int]
    rooms: list[Room]
    output_path: Path


def build_map_image(map_data: Map) -> None:
    """Build a map image.

    Compatible with `multiprocessing`.
    """
    images = ZipFile("data/berrycamp.zip")
    image = Image.new("RGBA", map_data.size)

    if (
        map_data.size[0] > MAX_IMAGE_DIMENSIONS
        or map_data.size[1] > MAX_IMAGE_DIMENSIONS
    ):
        print(f"Oversized map {map_data.output_path}: {map_data.size}")  # noqa: T201

    for room in map_data.rooms:
        image.paste(Image.open(images.open(room.zip_path)), (room.x, room.y))

    image.save(map_data.output_path)


if __name__ == "__main__":
    maps = []
    for checkpoint in iterate_checkpoints():
        canvas_offset = checkpoint.checkpoint_map_offset

        rooms = []
        for room in iterate_rooms(checkpoint):
            position = room.room_data["canvas"]["position"]
            rooms.append(
                Room(
                    f"berrycamp.github.io-dev/public/img/celeste/rooms/{room.chapter_id}/{room.side_id}/{room.room_id}.png",
                    position["x"] - canvas_offset["x"],
                    position["y"] - canvas_offset["y"],
                )
            )

        maps.append(
            Map(
                checkpoint.checkpoint_map_size,
                rooms,
                OUTPUT_PATH / f"{room.checkpoint_code}.png",
            )
        )

    with multiprocessing.Pool() as pool:
        pool.map(build_map_image, maps)
