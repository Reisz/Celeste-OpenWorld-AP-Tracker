"""Iterators for Berrycamp map data."""

import json
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Maps checkpoint code to list of sub checkpoints
# Each sub-checkpoint is a list of room ids
# Used to allow stitched maps to fit within the maximum size of 4096x4096
# NOTE: If the checkpoint code is not present, it is not split
# NOTE: For split checkpoints: If a room is not listed anywhere,
# it will not be included in the final map
CHECKPOINT_SPLIT_MAP = {
    "resort_a_ST": [
        [
            "s0",
            "s1",
            "s2",
            "s3",
            "0x-a",
            "00-a",
            "02-a",
            "02-b",
            "01-b",
            "00-b",
            "00-c",
            "0x-b",
        ],
        [
            "03-a",
            "04-b",
            "05-a",
            "06-a",
            "07-a",
            "07-b",
            "06-b",
            "06-c",
            "05-c",
            "08-c",
            "08-b",
        ],
    ],
    "resort_a_PS": [
        ["00-d", "roof00", "roof01", "roof02", "roof03", "roof04", "roof05"],
        ["roof06b", "roof06", "roof07"],
    ],
    "ridge_a_ST": [
        ["a-00", "a-01", "a-01x", "a-02", "a-03"],
        ["a-04", "a-05", "a-06", "a-07", "a-08", "a-10", "a-11", "a-09"],
    ],
    "ridge_a_OT": [
        ["c-00", "c-01", "c-02", "c-04", "c-05"],
        ["c-06", "c-06b", "c-09", "c-07", "c-08", "c-10"],
    ],
    "ridge_a_CF": [
        ["d-00", "d-00b", "d-01", "d-02", "d-03", "d-04", "d-05"],
        ["d-06", "d-07", "d-08", "d-09", "d-10"],
    ],
    "ridge_b_EOTS": [
        ["d-00", "d-01", "d-02"],
        ["d-03", "end"],
    ],
    "temple_a_DP": [
        [
            "b-00",
            "b-18",
            "b-01",
            "b-01c",
            "b-20",
            "b-21",
            "b-01b",
            "b-02",
            "b-03",
            "b-04",
            "b-05",
            "b-07",
            "b-08",
            "b-09",
            "b-10",
            "b-11",
            "b-12",
            "b-13",
            "b-17",
            "b-22",
            "b-06",
        ],
        [
            "b-19",
            "b-14",
            "b-15",
            "b-16",
            # "void" - ignored
        ],
    ],
    "temple_a_UR": [
        ["c-00", "c-01", "c-01b", "c-01c", "c-08b", "c-08"],
        ["c-10", "c-12", "c-07", "c-11", "c-09", "c-13"],
    ],
    "temple_a_RS": [
        ["e-00", "e-01", "e-02", "e-03", "e-04", "e-06", "e-05"],
        ["e-07", "e-08", "e-09", "e-10", "e-11"],
    ],
    "reflection_a_HL": [
        ["04", "04b", "04c", "04d", "04e", "05"],
        ["06", "07", "08a", "08b", "09", "10a", "10b", "11"],
        ["12a", "12b", "13", "14a", "14b", "15", "16a", "16b", "17"],
        ["18a", "18b", "19", "20"],
    ],
    "reflection_a_RF": [
        ["b-00", "b-00b", "b-00c", "b-01"],
        ["b-02"],
        ["b-02b", "b-03"],
    ],
    "reflection_a_RB": [
        [
            "boss-00",
            "boss-01",
            "boss-02",
            "boss-03",
            "boss-04",
            "boss-05",
            "boss-06",
            "boss-07",
        ],
        [
            "boss-08",
            "boss-09",
            "boss-10",
            "boss-11",
            "boss-12",
            "boss-13",
            "boss-14",
            "boss-15",
            "boss-16",
        ],
        ["boss-17", "boss-18", "boss-19", "boss-20"],
    ],
    "reflection_b_RF": [
        ["b-00", "b-01", "b-02", "b-03", "b-04"],
        ["b-05", "b-06", "b-07", "b-08", "b-10"],
    ],
    "reflection_b_RP": [
        ["d-00", "d-01", "d-02", "d-03"],
        ["d-04", "d-05"],
    ],
    "summit_a_1000M": [
        [
            "c-00",
            "c-01",
            "c-02",
            "c-03",
            "c-03b",
            "c-04",
            "c-05",
            "c-06",
            "c-06b",
            "c-06c",
        ],
        ["c-07", "c-07b", "c-08", "c-09"],
    ],
    "summit_a_1500M": [
        ["d-00", "d-01", "d-01b", "d-01c", "d-01d", "d-02", "d-03", "d-03b", "d-04"],
        ["d-05", "d-05b", "d-06", "d-07", "d-08", "d-09", "d-10", "d-10b", "d-11"],
    ],
    "summit_a_2000M": [
        ["e-00b", "e-00", "e-01", "e-01b", "e-01c", "e-02", "e-03", "e-04", "e-05"],
        ["e-06", "e-07", "e-08", "e-09", "e-11", "e-12", "e-10", "e-10b", "e-13"],
    ],
    "summit_a_2500M": [
        ["f-00", "f-01", "f-02", "f-02b", "f-04", "f-03", "f-05", "f-06", "f-07"],
        ["f-08", "f-08b", "f-08d", "f-08c", "f-09", "f-10", "f-10b", "f-11"],
    ],
    "summit_a_3000M": [
        ["g-00"],
        ["g-00b"],
        ["g-01"],
        ["g-02", "g-03"],
    ],
    "summit_b_3000M": [
        ["g-00", "g-01"],
        ["g-02", "g-03"],
    ],
    "summit_c_BG": [
        ["01", "02"],
        ["03"],
    ],
    "epilogue_a_BG": [["outside", "bridge", "secret"]],  # "inside" - ignored
    "core_a_HOTM": [
        ["d-00", "d-01", "d-02", "d-03", "d-04", "d-05", "d-06"],
        ["d-07", "d-08", "d-09", "d-10", "d-10b"],
        ["d-10c", "d-11"],
        ["space"],
    ],
    "core_b_BOF": [
        ["b-00", "b-01", "b-02"],
        ["b-03", "b-04", "b-05"],
    ],
    "core_b_HB": [
        ["c-01", "c-02", "c-03", "c-04"],
        ["c-05", "c-06", "c-08", "c-07"],
        ["space"],
    ],
    "core_c_BG": [
        ["intro", "00", "01"],
        ["02"],
    ],
}

# Maps room code to crop region
# Used to reduce the size of stitched maps by removing inaccessible regions
# NOTE: Missing fields use base image geometry
# NOTE: Cropping may only occur on the outside edges of a stitched map, otherwise the
# stitching will fail
ROOM_CROPS = {
    "city_a_10zb": {
        "x": 235,
    },
    "site_a_9b": {
        "x": 160,
        "y": 145,
        "width": 340,
    },
    "resort_a_roof07": {
        "width": 235,
        "height": 184,
    },
    "resort_b_back": {
        "x": 1235,
    },
    "ridge_a_d-10": {
        "y": 744,
        "width": 220,
    },
    "temple_a_a-00x": {
        "x": 480,
    },
    "reflection_a_start": {
        "height": 2700,
    },
    "summit_a_a-06": {
        "y": 290,
    },
    "summit_a_b-09": {
        "y": 540,
    },
    "summit_a_c-09": {
        "y": 500,
    },
    "summit_a_d-11": {
        "y": 425,
    },
    "summit_a_e-01b": {
        "x": 136,
    },
    "summit_a_e-13": {
        "y": 515,
    },
    "summit_a_f-11": {
        "y": 430,
    },
    "summit_a_g-00": {
        "y": 475,
    },
    "summit_a_g-00b": {
        "y": 565,
    },
    "summit_a_g-01": {
        "y": 310,
        "width": 2495,
    },
    "summit_a_g-02": {
        "x": 125,
    },
    "summit_a_g-03": {
        "x": 125,
        "y": 325,
        "width": 1775,
    },
    "summit_b_a-03": {
        "y": 605,
    },
    "summit_b_b-03": {
        "y": 580,
    },
    "summit_b_c-03": {
        "y": 870,
    },
    "summit_b_d-03": {
        "y": 455,
    },
    "summit_b_e-03": {
        "y": 500,
    },
    "summit_b_f-03": {
        "y": 715,
    },
    "summit_b_g-01": {
        "y": 185,
    },
    "summit_b_g-02": {
        "x": 60,
        "width": 1746,
    },
    "summit_b_g-03": {
        "x": 280,
        "width": 550,
    },
    "core_b_c-04": {
        "y": 510,
    },
}


@dataclass
class Position:
    """Position, as defined by the Berrycamp data."""

    x: int
    y: int


@dataclass
class ChapterData:
    """Berrycamp data for a chapter."""

    chapter_data: dict[str, Any]

    @property
    def chapter_id(self) -> str:
        """Return the chapter id."""
        return str(self.chapter_data["id"])


def iterate_chapters() -> Iterator[ChapterData]:
    """Iterate over all chapters without sides."""
    with Path("data/celeste.json").open() as f:
        data = json.load(f)
    return (
        ChapterData(chapter)
        for chapter in data["chapters"]
        if chapter["id"] != "farewell"  # TODO(Reisz): #28 Enable farewell
    )


@dataclass
class SideData(ChapterData):
    """Berrycamp data for a chapters side."""

    side_data: dict[str, Any]

    @property
    def side_id(self) -> str:
        """Return the side id."""
        return str(self.side_data["id"])

    @property
    def side_code(self) -> str:
        """Return a uniquely identifying side code."""
        return f"{self.chapter_id}_{self.side_id}"


def iterate_sides(chapter: ChapterData | None = None) -> Iterator[SideData]:
    """Iterate over all chapters and sides or all sides of a chapter."""
    iterator = [chapter] if chapter is not None else iterate_chapters()
    for data in iterator:
        for side in data.chapter_data["sides"]:
            yield SideData(data.chapter_data, side)


@dataclass
class CheckpointData(SideData):
    """Berrycamp data for a checkpoint."""

    checkpoint_index: int
    checkpoint_subindex: int | None
    checkpoint_data: dict[str, Any]

    @property
    def checkpoint_id(self) -> str:
        """Return the checkpoint id."""
        suffix = (
            f"-{self.checkpoint_subindex}"
            if self.checkpoint_subindex is not None
            else ""
        )
        return f"{self.checkpoint_data['abbreviation']}{suffix}"

    @property
    def checkpoint_code(self) -> str:
        """Return a uniquely identifying checkpoint code."""
        return f"{self.side_code}_{self.checkpoint_id}"

    @property
    def checkpoint_name(self) -> str:
        """Return the checkpoint name."""
        suffix = (
            f" - {self.checkpoint_subindex + 1}"
            if self.checkpoint_subindex is not None
            else ""
        )
        return f"{self.checkpoint_data['name']}{suffix}"

    @property
    def checkpoint_map_offset(self) -> Position:
        """Return the top-left position of the top-left room."""
        positions = [room.room_position for room in iterate_rooms(self)]
        return Position(
            x=min(position.x for position in positions),
            y=min(position.y for position in positions),
        )


def iterate_checkpoints(side: SideData | None = None) -> Iterator[CheckpointData]:
    """Iterate over all checkpoints or all checkpoints of a side."""
    iterator = [side] if side is not None else iterate_sides()
    for data in iterator:
        for index, checkpoint in enumerate(data.side_data["checkpoints"]):
            checkpoint_data = CheckpointData(
                data.chapter_data, data.side_data, index, None, checkpoint
            )

            if checkpoint_data.checkpoint_code not in CHECKPOINT_SPLIT_MAP:
                yield checkpoint_data
            else:
                splits = CHECKPOINT_SPLIT_MAP[checkpoint_data.checkpoint_code]
                for sub_index in range(len(splits)):
                    checkpoint_data = CheckpointData(
                        data.chapter_data, data.side_data, index, sub_index, checkpoint
                    )
                    yield checkpoint_data


@dataclass
class RoomData(CheckpointData):
    """Berrycamp data for a room."""

    room_id: int
    room_data: dict[str, Any]

    @property
    def room_position(self) -> Position:
        """Return room position in subchapter in pillow Image.paste box format."""
        position = self.room_data["canvas"]["position"]
        crop = self.room_crop
        return Position(
            position["x"] + crop[0],
            position["y"] + crop[1],
        )

    @property
    def room_crop(self) -> tuple[int, int, int, int]:
        """Return room crop in pillow Image.crop format."""
        crop = ROOM_CROPS.get(self.room_code, {})
        x = crop.get("x", 0)
        y = crop.get("y", 0)
        w = crop.get("width", self.room_data["canvas"]["size"]["width"] - x)
        h = crop.get("height", self.room_data["canvas"]["size"]["height"] - y)

        return (x, y, x + w, y + h)

    @property
    def room_offset(self) -> Position:
        """Return offset of entities in room relative to subchapter."""
        position = self.room_position
        crop = self.room_crop

        position.x -= crop[0]
        position.y -= crop[1]

        return position

    @property
    def room_code(self) -> str:
        """Return a uniquely identifying room code."""
        return f"{self.side_code}_{self.room_id}"


def iterate_rooms(checkpoint: CheckpointData | None = None) -> Iterator["RoomData"]:
    """Iterate over all rooms or all rooms of a checkpoint."""
    iterator = [checkpoint] if checkpoint is not None else iterate_checkpoints()
    for data in iterator:
        room_iterator = data.side_data["rooms"].items()
        if data.checkpoint_subindex is not None:
            ids = CHECKPOINT_SPLIT_MAP[
                f"{data.side_code}_{data.checkpoint_data['abbreviation']}"
            ][data.checkpoint_subindex]
            room_iterator = (
                (room_id, data.side_data["rooms"][room_id]) for room_id in ids
            )
        for room_id, room in room_iterator:
            if room["checkpointNo"] == data.checkpoint_index:
                yield RoomData(
                    data.chapter_data,
                    data.side_data,
                    data.checkpoint_index,
                    data.checkpoint_subindex,
                    data.checkpoint_data,
                    room_id,
                    room,
                )
