"""Generates maps and maps tab layout."""

import json
from pathlib import Path
from typing import Any

from lib.iterators import iterate_chapters, iterate_checkpoints, iterate_sides

Path("tracker/maps").mkdir(parents=True, exist_ok=True)
Path("tracker/layouts").mkdir(parents=True, exist_ok=True)

with Path("data/celeste.json").open() as f:
    data = json.load(f)
maps = []

maps_tabs: list[dict[str, Any]] = []
maps_layout = {
    "maps": {
        "type": "tabbed",
        "tabs": maps_tabs,
    },
}

for chapter in iterate_chapters():
    chapter_tabs: list[dict[str, Any]] = []
    chapter_container = {
        "title": chapter.chapter_data["name"],
        "content": {
            "type": "tabbed",
            "tabs": chapter_tabs,
        },
    }
    maps_tabs.append(chapter_container)

    for side in iterate_sides(chapter):
        side_tabs: list[dict[str, Any]] = []
        side_container = {
            "title": side.side_data["name"],
            "content": {
                "type": "tabbed",
                "tabs": side_tabs,
            },
        }

        if len(chapter.chapter_data["sides"]) == 1:
            side_tabs = chapter_tabs
            side_container = chapter_container
        else:
            chapter_tabs.append(side_container)

        for checkpoint in iterate_checkpoints(side):
            maps.append(
                {
                    "name": checkpoint.checkpoint_code,
                    "location_size": 12,
                    "location_border_thickness": 2,
                    "location_shape": "rect",
                    "img": f"images/maps/{checkpoint.checkpoint_code}.png",
                }
            )

            if len([*iterate_checkpoints(side)]) == 1:
                side_container["content"]["type"] = "map"
                side_container["content"]["maps"] = [checkpoint.checkpoint_code]
                del side_container["content"]["tabs"]
            else:
                side_tabs.append(
                    {
                        "title": checkpoint.checkpoint_name,
                        "content": {
                            "type": "map",
                            "maps": [checkpoint.checkpoint_code],
                        },
                    }
                )

with Path("tracker/maps.json").open("w") as f:
    json.dump(maps, f)
with Path("tracker/layouts/maps.json").open("w") as f:
    json.dump(maps_layout, f)
