import json
from pathlib import Path
from typing import Any

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

for chapter in data["chapters"]:
    if chapter["id"] == "farewell":
        continue

    chapter_tabs: list[dict[str, Any]] = []
    chapter_container = {
        "title": chapter["name"],
        "content": {
            "type": "tabbed",
            "tabs": chapter_tabs,
        },
    }
    maps_tabs.append(chapter_container)

    for side in chapter["sides"]:
        side_tabs: list[dict[str, Any]] = []
        side_container = {
            "title": side["name"],
            "content": {
                "type": "tabbed",
                "tabs": side_tabs,
            },
        }

        if len(chapter["sides"]) == 1:
            side_tabs = chapter_tabs
            side_container = chapter_container
        else:
            chapter_tabs.append(side_container)

        for checkpoint in side["checkpoints"]:
            name = f"{chapter['id']}_{side['id']}_{checkpoint['abbreviation']}"

            maps.append(
                {
                    "name": name,
                    "location_size": 12,
                    "location_border_thickness": 2,
                    "location_shape": "rect",
                    "img": f"images/maps/{name}.png",
                }
            )

            if len(side["checkpoints"]) == 1:
                side_container["content"]["type"] = "map"
                side_container["content"]["maps"] = [name]
                del side_container["content"]["tabs"]
            else:
                side_tabs.append(
                    {
                        "title": checkpoint["name"],
                        "content": {
                            "type": "map",
                            "maps": [name],
                        },
                    }
                )

with Path("tracker/maps/maps.json").open("w") as f:
    json.dump(maps, f)
with Path("tracker/layouts/maps.json").open("w") as f:
    json.dump(maps_layout, f)
