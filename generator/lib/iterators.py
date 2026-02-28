"""Iterators for Berrycamp map data."""

import json
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ChapterData:
    """Berrycamp data for a chapter."""

    chapter_data: dict[str, Any]

    @property
    def chapter_id(self) -> str:
        """Return the chapter id."""
        return str(self.chapter_data["id"])


def iterate_chapters() -> Iterator["ChapterData"]:
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


def iterate_sides(chapter: ChapterData | None = None) -> Iterator["SideData"]:
    """Iterate over all chapters and sides or all sides of a chapter."""
    iterator = [chapter] if chapter is not None else iterate_chapters()
    for data in iterator:
        for side in data.chapter_data["sides"]:
            yield SideData(data.chapter_data, side)


@dataclass
class CheckpointData(SideData):
    """Berrycamp data for a checkpoint."""

    checkpoint_index: int
    checkpoint_data: dict[str, Any]

    @property
    def checkpoint_id(self) -> str:
        """Return the checkpoint id."""
        return str(self.checkpoint_data["abbreviation"])

    @property
    def checkpoint_code(self) -> str:
        """Return a uniquely identifying checkpoint code."""
        return f"{self.side_code}_{self.checkpoint_id}"


def iterate_checkpoints(side: SideData | None = None) -> Iterator["CheckpointData"]:
    """Iterate over all checkpoints or all checkpoints of a side."""
    iterator = [side] if side is not None else iterate_sides()
    for data in iterator:
        for index, checkpoint in enumerate(data.side_data["checkpoints"]):
            yield CheckpointData(data.chapter_data, data.side_data, index, checkpoint)


@dataclass
class RoomData(CheckpointData):
    """Berrycamp data for a room."""

    room_id: int
    room_data: dict[str, Any]

    @property
    def room_code(self) -> str:
        """Return a uniquely identifying room code."""
        return f"{self.side_code}_{self.room_id}"


def iterate_rooms(checkpoint: CheckpointData | None = None) -> Iterator["RoomData"]:
    """Iterate over all rooms or all rooms of a checkpoint."""
    iterator = [checkpoint] if checkpoint is not None else iterate_checkpoints()
    for data in iterator:
        for room_id, room in data.side_data["rooms"].items():
            if room["checkpointNo"] == data.checkpoint_index:
                yield RoomData(
                    data.chapter_data,
                    data.side_data,
                    data.checkpoint_index,
                    data.checkpoint_data,
                    room_id,
                    room,
                )
