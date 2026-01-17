import json

HEART_COLORS = {
    "a": "blue",
    "b": "red",
    "c": "yellow",
}

data = json.load(open("data/celeste.json"))

locations_children = []
locations = [{"children": locations_children}]

for chapter in data["chapters"]:
    if chapter["id"] == "farewell":
        continue

    for side in chapter["sides"]:
        for checkpoint_idx, checkpoint in enumerate(side["checkpoints"]):
            id = f"{chapter['id']}_{side['id']}_{checkpoint['abbreviation']}"
            canvas_offset = checkpoint["canvas"]["position"]

            for room_id, room in side["rooms"].items():
                if room["checkpointNo"] != checkpoint_idx:
                    continue

                room_offset = room["canvas"]["position"]

                def loc(entity):
                    return {
                        "map": id,
                        "x": room_offset["x"] - canvas_offset["x"] + entity["x"],
                        "y": room_offset["y"] - canvas_offset["y"] + entity["y"],
                    }

                for entity in room["entities"].get("berry", []):
                    locations_children.append(
                        {
                            "name": f"Strawberry {entity['id']}",
                            "map_locations": [loc(entity)],
                            "sections": [{}],
                            "chest_unopened_img": "images/locations/strawberry.png",
                            "chest_opened_img": "images/locations/strawberry_collected.png",
                        }
                    )

                for entity in room["entities"].get("golden", []):
                    locations_children.append(
                        {
                            "name": "Golden Strawberry",
                            "map_locations": [loc(entity)],
                            "sections": [{}],
                            "chest_unopened_img": "images/locations/golden_strawberry.png",
                            "chest_opened_img": "images/locations/golden_strawberry_collected.png",
                        }
                    )

                for entity in room["entities"].get("cassette", []):
                    locations_children.append(
                        {
                            "name": "Cassette",
                            "map_locations": [loc(entity)],
                            "sections": [{}],
                            "chest_unopened_img": "images/locations/cassette.png",
                            "chest_opened_img": "images/locations/cassette_collected.png",
                        }
                    )

                for entity in room["entities"].get("heart", []):
                    heart_color = HEART_COLORS[side["id"]]
                    locations_children.append(
                        {
                            "name": "Heart",
                            "map_locations": [loc(entity)],
                            "sections": [{}],
                            "chest_unopened_img": f"images/locations/{heart_color}_heart.png",
                            "chest_opened_img": f"images/locations/{heart_color}_heart_collected.png",
                        }
                    )

json.dump(locations, open("tracker/locations.json", "w"))
