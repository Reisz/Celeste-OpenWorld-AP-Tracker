import pathlib
import json

pathlib.Path("tracker/locations").mkdir(parents=True, exist_ok=True)

data = json.load(open("data/celeste.json"))

berries_children = []
berries = [{"children": berries_children}]

goldens_children = []
goldens = [{"children": goldens_children}]

cassettes_children = []
cassettes = [{"children": cassettes_children}]

hearts_children = []
hearts = [{"children": hearts_children}]

for chapter in data["chapters"]:
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
                    berries_children.append(
                        {
                            "name": f"Strawberry {entity['id']}",
                            "map_locations": [loc(entity)],
                            "sections": [{}],
                        }
                    )

                for entity in room["entities"].get("golden", []):
                    goldens_children.append(
                        {
                            "name": "Golden Strawberry",
                            "map_locations": [loc(entity)],
                            "sections": [{}],
                        }
                    )

                for entity in room["entities"].get("cassette", []):
                    cassettes_children.append(
                        {
                            "name": "Cassette",
                            "map_locations": [loc(entity)],
                            "sections": [{}],
                        }
                    )

                for entity in room["entities"].get("heart", []):
                    hearts_children.append(
                        {
                            "name": "Heart",
                            "map_locations": [loc(entity)],
                            "sections": [{}],
                        }
                    )


json.dump(berries, open("tracker/locations/berries.json", "w"))
json.dump(goldens, open("tracker/locations/goldens.json", "w"))
json.dump(cassettes, open("tracker/locations/cassettes.json", "w"))
json.dump(hearts, open("tracker/locations/hearts.json", "w"))
