"""Generates map images from Berrycamp data and room images."""

import json
import multiprocessing
from dataclasses import dataclass
from pathlib import Path
from zipfile import ZipFile

from lib.iterators import (
    Position,
    RoomData,
    checkpoint_map_size,
    iterate_checkpoints,
    iterate_rooms,
)
from PIL import Image

MAX_IMAGE_DIMENSIONS = 4096

OUTPUT_PATH = Path("tracker/images/maps")
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

with Path("data/celeste.json").open() as f:
    data = json.load(f)


@dataclass
class Map:
    """Map image to be built."""

    offset: Position
    size: tuple[int, int]
    rooms: list[RoomData]
    output_path: Path


def build_map_image(map_data: Map) -> None:
    """Build a map image.

    Compatible with `multiprocessing`.
    """
    offset = map_data.offset
    size = map_data.size

    images = ZipFile("data/berrycamp.zip")
    image = Image.new("RGBA", size)

    if size[0] > MAX_IMAGE_DIMENSIONS or size[1] > MAX_IMAGE_DIMENSIONS:
        print(f"Oversized map {map_data.output_path}: {size}")  # noqa: T201

    for room in map_data.rooms:
        zip_path = (
            "berrycamp.github.io-dev/public/img/celeste/rooms/"
            f"{room.chapter_id}/{room.side_id}/{room.room_id}.png"
        )
        position = room.room_position
        image.paste(
            Image.open(images.open(zip_path)).crop(room.room_crop),
            (position.x - offset.x, position.y - offset.y),
        )

    image.save(map_data.output_path)


if __name__ == "__main__":
    maps = [
        Map(
            checkpoint.checkpoint_map_offset,
            checkpoint_map_size(checkpoint),
            list(iterate_rooms(checkpoint)),
            OUTPUT_PATH / f"{checkpoint.checkpoint_code}.png",
        )
        for checkpoint in iterate_checkpoints()
    ]

    with multiprocessing.Pool() as pool:
        pool.map(build_map_image, maps)
