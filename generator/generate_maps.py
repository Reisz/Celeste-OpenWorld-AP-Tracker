import json
import pathlib

pathlib.Path("tracker/maps").mkdir(parents=True, exist_ok=True)
pathlib.Path("tracker/layouts").mkdir(parents=True, exist_ok=True)

data = json.load(open("data/celeste.json"))
maps = []

maps_tabs = []
maps_layout = {
    "maps": {
        "type": "tabbed",
        "tabs": maps_tabs,
    },
}

for chapter in data["chapters"]:
    if chapter["id"] == "farewell":
        continue

    chapter_tabs = []
    chapter_container = {
        "title": chapter["name"],
        "content": {
            "type": "tabbed",
            "tabs": chapter_tabs,
        },
    }
    maps_tabs.append(chapter_container)

    for side in chapter["sides"]:
        side_tabs = []
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

        for checkpoint_idx, checkpoint in enumerate(side["checkpoints"]):
            id = f"{chapter['id']}_{side['id']}_{checkpoint['abbreviation']}"

            maps.append(
                {
                    "name": id,
                    "location_size": 12,
                    "location_border_thickness": 2,
                    "location_shape": "rect",
                    "img": f"images/maps/{id}.png",
                }
            )

            if len(side["checkpoints"]) == 1:
                side_container["content"]["type"] = "map"
                side_container["content"]["maps"] = [id]
                del side_container["content"]["tabs"]
            else:
                side_tabs.append(
                    {
                        "title": checkpoint["name"],
                        "content": {
                            "type": "map",
                            "maps": [id],
                        },
                    }
                )

json.dump(maps, open("tracker/maps/maps.json", "w"))
json.dump(maps_layout, open("tracker/layouts/maps.json", "w"))
