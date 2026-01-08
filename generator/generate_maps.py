import json
import pathlib

pathlib.Path("tracker/maps").mkdir(parents=True, exist_ok=True)
pathlib.Path("tracker/layouts").mkdir(parents=True, exist_ok=True)

data = json.load(open("data/celeste.json"))
maps = []

tracker_tabs = []
tracker = {
    "tracker_default": {
        "type": "container",
        "background": "#000000",
        "content": {
            "type": "tabbed",
            "content": tracker_tabs,
        },
    }
}

for chapter in data["chapters"]:
    chapter_tabs = []
    chapter_container = {
        "title": chapter["name"],
        "type": "tabbed",
        "content": chapter_tabs,
    }
    tracker_tabs.append(chapter_container)

    for side in chapter["sides"]:
        side_tabs = []
        side_container = {
            "title": side["name"],
            "type": "tabbed",
            "content": side_tabs,
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
                side_container["type"] = "map"
                side_container["maps"] = [id]
                del side_container["content"]
            else:
                side_tabs.append(
                    {
                        "title": checkpoint["name"],
                        "type": "map",
                        "maps": [id],
                    }
                )

json.dump(maps, open("tracker/maps/maps.json", "w"))
json.dump(tracker, open("tracker/layouts/tracker.json", "w"))
