import json
import pathlib

HEART_COLORS = {
    "a": "blue",
    "b": "red",
    "c": "yellow",
}

BERRY_MAPPING = {
    # https://berrycamp.github.io/map/celeste/site/a?room=d2
    "site_d2_9": 2,
    "site_d2_31": 1,
    # https://berrycamp.github.io/map/celeste/resort/a?room=s2
    "resort_s2_6": 2,
    "resort_s2_18": 1,
    # https://berrycamp.github.io/map/celeste/resort/a?room=03-b
    "resort_03-b_1": 2,
    "resort_03-b_25": 1,
    # https://berrycamp.github.io/map/celeste/resort/a?room=roof06
    "resort_roof06_276": 1,  # TODO: Order not clear from level data
    "resort_roof06_308": 2,
    # https://berrycamp.github.io/map/celeste/ridge/a?room=b-01
    "ridge_b-01_6": 1,  # TODO: Order not clear from level data
    "ridge_b-01_13": 2,
    # https://berrycamp.github.io/map/celeste/ridge/a?room=b-02
    "ridge_b-02_20": 1,
    "ridge_b-02_58": 2,
    # https://berrycamp.github.io/map/celeste/temple/a?room=a-01
    "temple_a-01_164": 1,  # TODO: Order not clear from level data
    "temple_a-01_256": 2,
    # https://berrycamp.github.io/map/celeste/temple/a?room=b-17
    "temple_b-17_10": 2,
    "temple_b-17_14": 1,
    # https://berrycamp.github.io/map/celeste/temple/a?room=b-20
    "temple_b-20_72": 1,
    "temple_b-20_183": 2,
    # https://berrycamp.github.io/map/celeste/temple/a?room=d-04
    "temple_d-04_16": 1,
    "temple_d-04_122": 2,
    # https://berrycamp.github.io/map/celeste/temple/a?room=d-15
    "temple_d-15_217": 2,
    "temple_d-15_335": 1,
    # https://berrycamp.github.io/map/celeste/summit/a?room=a-04b
    "summit_a-04b_85": 2,
    "summit_a-04b_136": 1,
    # https://berrycamp.github.io/map/celeste/summit/a?room=f-11
    "summit_f-11_1068": 2,  # TODO: Order between 1 and 2 not clear from level data
    "summit_f-11_1229": 3,
    "summit_f-11_1238": 1,
    # https://berrycamp.github.io/map/celeste/summit/a?room=g-00b
    "summit_g-00b_37": 1,
    "summit_g-00b_114": 3,
    "summit_g-00b_127": 2,
    # https://berrycamp.github.io/map/celeste/summit/a?room=g-01
    "summit_g-01_66": 1,
    "summit_g-01_279": 3,  # TODO: Order between 2 and 3 not clear from level data
    "summit_g-01_342": 2,
}

data = json.load(open("data/celeste.json"))
ids = json.load(open("data/ids.json"))["location_name_to_id"]

locations_children = []
locations = [{"children": locations_children}]

mappings = {}

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

                berry_count = len(room["entities"].get("berry", []))
                for entity in room["entities"].get("berry", []):
                    berry_id = f"{chapter['id']}_{room_id}_{entity['id']}"
                    suffix = f" {BERRY_MAPPING[berry_id]}" if berry_count > 1 else ""
                    name = f"{chapter['name']} {side['name']} [Room {room_id}] Strawberry{suffix}"
                    locations_children.append(
                        {
                            "name": f"{chapter['name']} {side['name']} [Room {room_id}] Strawberry{suffix}",
                            "map_locations": [loc(entity)],
                            "sections": [{}],
                            "chest_unopened_img": "images/locations/strawberry.png",
                            "chest_opened_img": "images/locations/strawberry_collected.png",
                        }
                    )

                    id_name = f"{chapter['name']} {side['name']} - Room {room_id} Strawberry{suffix}"
                    mappings[ids[id_name]] = name

                for entity in room["entities"].get("golden", []):
                    name = f"{chapter['name']} {side['name']} Golden Strawberry"
                    locations_children.append(
                        {
                            "name": name,
                            "map_locations": [loc(entity)],
                            "sections": [{}],
                            "chest_unopened_img": "images/locations/golden_strawberry.png",
                            "chest_opened_img": "images/locations/golden_strawberry_collected.png",
                        }
                    )

                    id_name = f"{chapter['name']} {side['name']} - Golden Strawberry"
                    mappings[ids[id_name]] = name

                for entity in room["entities"].get("cassette", []):
                    name = f"{chapter['name']} Cassette"
                    locations_children.append(
                        {
                            "name": name,
                            "map_locations": [loc(entity)],
                            "sections": [{}],
                            "chest_unopened_img": "images/locations/cassette.png",
                            "chest_opened_img": "images/locations/cassette_collected.png",
                        }
                    )

                    id_name = f"{chapter['name']} {side['name']} - Cassette"
                    mappings[ids[id_name]] = name

                for entity in room["entities"].get("heart", []):
                    # Skip unreachable heart in final checkpoint of Old Site A
                    if (
                        chapter["id"] == "site"
                        and side["id"] == "a"
                        and checkpoint["abbreviation"] != "ST"
                    ):
                        continue

                    heart_color = HEART_COLORS[side["id"]]
                    name = f"{chapter['name']} {heart_color.title()} Heart"
                    locations_children.append(
                        {
                            "name": name,
                            "map_locations": [loc(entity)],
                            "sections": [{}],
                            "chest_unopened_img": f"images/locations/{heart_color}_heart.png",
                            "chest_opened_img": f"images/locations/{heart_color}_heart_collected.png",
                        }
                    )

                    hidden_heart = chapter["id"] != "core" and side["id"] == "a"
                    id_name = f"{chapter['name']} {side['name']} - {'Crystal Heart' if hidden_heart else 'Level Clear'}"
                    mappings[ids[id_name]] = name

json.dump(locations, open("tracker/locations.json", "w"))

mappings = ",".join(f'[{k}] = "@{v}/"' for k, v in mappings.items())

pathlib.Path("tracker/scripts/mappings").mkdir(parents=True, exist_ok=True)
f = open("tracker/scripts/mappings/locations.lua", "w")
f.write("LOCATION_MAPPINGS={")
f.write(mappings)
f.write("}")
