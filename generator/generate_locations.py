import json
import pathlib
from collections import defaultdict
from dataclasses import dataclass

HEART_COLORS = {
    "a": "blue",
    "b": "red",
    "c": "yellow",
}

# Berrycamp `<chapter>` -> AP chapter index
CHAPTER_MAP = {
    "prologue": 0,
    "city": 1,
    "site": 2,
    "resort": 3,
    "ridge": 4,
    "temple": 5,
    "reflection": 6,
    "summit": 7,
    "epilogue": 8,
    "core": 9,
    "farewell": 10,
}

# Berrycamp `<chapter>_<room>_<berry>` -> AP berry index
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


@dataclass(frozen=True)
class ApRule:
    rule: frozenset[frozenset[str]] = frozenset()

    @staticmethod
    def from_ap(rule: list[list[str]]) -> "ApRule":
        if not rule:
            return ApRule()
        return ApRule(frozenset(frozenset(group) for group in rule))

    def to_poptracker(self) -> list[str]:
        return [",".join(group) for group in self.rule]

    def __and__(self, other: "ApRule") -> "ApRule":
        if not self.rule:
            return other
        if not other.rule:
            return self

        return ApRule(frozenset(a | b for a in self.rule for b in other.rule))

    def __or__(self, other: "ApRule") -> "ApRule":
        return ApRule(self.rule | other.rule)


@dataclass
class ApRegionConnection:
    dest_region: str
    rule: ApRule


@dataclass
class ApRegion:
    entity_rules: dict[str, ApRule]
    region_connections: list[ApRegionConnection]
    rule: ApRule = ApRule()


@dataclass
class ApRoom:
    regions: dict[str, ApRegion]


@dataclass
class ApChapter:
    rooms: dict[str, ApRoom]


@dataclass(frozen=True)
class RegionIndex:
    room_id: str
    region_id: str


@dataclass(frozen=True)
class Route:
    route: tuple[RegionIndex]

    @staticmethod
    def start(chapter_data) -> "Route":
        start_room = next(
            x for x in chapter_data["rooms"] if x["checkpoint"] == "Start"
        )
        return Route(
            (RegionIndex(start_room["name"], start_room["checkpoint_region"]),)
        )

    def back(self) -> RegionIndex:
        return self.route[-1]

    def extend(self, region_index: RegionIndex) -> "Route | None":
        if region_index in self.route:
            return None
        return Route(self.route + (region_index,))

    def extended_to_region(self, region_id: str) -> "Route | None":
        return self.extend(RegionIndex(self.back().room_id, region_id))


@dataclass
class Todo:
    route: list[RegionIndex]
    rule: ApRule


ap_chapters: dict[str, ApChapter] = {}
for chapter_data in json.load(open("data/CelesteLevelData.json"))["levels"]:
    if chapter_data["name"].startswith("10"):
        continue

    print(f"Calculating rules for {chapter_data['display_name']}")

    rooms = {}
    ap_chapters[chapter_data["name"]] = ApChapter(rooms=rooms)

    # Convert individual room data
    for room_data in chapter_data["rooms"]:
        rooms[room_data["name"]] = ApRoom(
            {
                region_data["name"]: ApRegion(
                    entity_rules={
                        x["display_name"]: ApRule.from_ap(x["rule"])
                        for x in region_data.get("locations", [])
                    },
                    region_connections=[
                        ApRegionConnection(
                            dest_region=x["dest"], rule=ApRule.from_ap(x["rule"])
                        )
                        for x in region_data["connections"]
                    ],
                )
                for region_data in room_data["regions"]
            }
        )

    # Prepare room connections
    doors = defaultdict(list)
    for conn in chapter_data["room_connections"]:
        doors[RegionIndex(conn["source_room"], conn["source_door"])].append(
            RegionIndex(conn["dest_room"], conn["dest_door"])
        )

    # Graph traversal
    todo = [Todo(Route.start(chapter_data), ApRule())]
    while todo:
        current_todo = todo.pop()

        # Add calculated rule to current region
        rooms[current_todo.route.back().room_id].regions[
            current_todo.route.back().region_id
        ].rule |= current_todo.rule

        # Schedule connections within room
        current_room = rooms[current_todo.route.back().room_id]
        current_region = current_room.regions[current_todo.route.back().region_id]
        for conn in current_region.region_connections:
            route = current_todo.route.extended_to_region(conn.dest_region)
            if route is not None:
                todo.append(Todo(route, current_todo.rule & conn.rule))

        # Schedule connections to other rooms
        for conn in doors[current_todo.route.back()]:
            route = current_todo.route.extend(conn)
            if route is not None:
                todo.append(Todo(route, current_todo.rule))


def get_access_rules(chapter, side, room_id, entity):
    chapter = ap_chapters[f"{CHAPTER_MAP[chapter['id']]}{side['id']}"]
    region, region_id = next(
        (region, region_id)
        for region_id, region in chapter.rooms[room_id].regions.items()
        if entity in region.entity_rules
    )

    return (region.rule & region.entity_rules[entity]).to_poptracker()


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
                            "access_rules": get_access_rules(
                                chapter, side, room_id, f"Strawberry{suffix}"
                            ),
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
                            "access_rules": get_access_rules(
                                chapter, side, room_id, "Cassette"
                            ),
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
                    ap_name = (
                        "Crystal Heart"
                        if side["id"] == "a" and chapter["id"] != "core"
                        else "Level Clear"
                    )
                    locations_children.append(
                        {
                            "name": name,
                            "access_rules": get_access_rules(
                                chapter, side, room_id, ap_name
                            ),
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
