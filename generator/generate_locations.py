import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

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
    "resort_roof06_276": 1,  # TODO(Reisz): #2 Order not clear from level data
    "resort_roof06_308": 2,
    # https://berrycamp.github.io/map/celeste/ridge/a?room=b-01
    "ridge_b-01_6": 1,  # TODO(Reisz): #2 Order not clear from level data
    "ridge_b-01_13": 2,
    # https://berrycamp.github.io/map/celeste/ridge/a?room=b-02
    "ridge_b-02_20": 1,
    "ridge_b-02_58": 2,
    # https://berrycamp.github.io/map/celeste/temple/a?room=a-01
    "temple_a-01_164": 1,  # TODO(Reisz): #2 Order not clear from level data
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
    # TODO(Reisz): #2 Order between 1 and 2 not clear from level data
    "summit_f-11_1068": 2,
    "summit_f-11_1229": 3,
    "summit_f-11_1238": 1,
    # https://berrycamp.github.io/map/celeste/summit/a?room=g-00b
    "summit_g-00b_37": 1,
    "summit_g-00b_114": 3,
    "summit_g-00b_127": 2,
    # https://berrycamp.github.io/map/celeste/summit/a?room=g-01
    "summit_g-01_66": 1,
    # TODO(Reisz): #2 Order between 2 and 3 not clear from level data
    "summit_g-01_279": 3,
    "summit_g-01_342": 2,
}

# Location measured at the bottom-left pixel of the dark band separating bow and shaft
KEYS = {
    "resort_a_s3": [
        {
            "name": "Front Door Key",
            "x": 103,
            "y": 239,
        },
    ],
    "resort_a_02-b": [
        {
            "name": "Hallway Key 1",
            "x": 203,
            "y": 139,
        },
    ],
    "resort_a_07-b": [
        {
            "name": "Hallway Key 2",
            "x": 231,
            "y": 135,
        },
    ],
    "resort_a_09-b": [
        {
            "name": "Huge Mess Key",
            "x": 319,
            "y": 183,
        },
    ],
    "resort_a_02-c": [
        {
            "name": "Presidential Suite Key",
            "x": 63,
            "y": 119,
        },
    ],
    "temple_a_a-08": [
        {
            "name": "Entrance Key",
            "x": 255,
            "y": 255,
        },
    ],
    "temple_a_b-04": [
        {
            "name": "Depths Key",
            "x": 159,
            "y": 55,
        },
    ],
    "temple_a_d-04": [
        {
            "name": "Search Key 1",
            "x": 199,
            "y": 151,
        },
        {
            "name": "Search Key 2",
            "x": 279,
            "y": 151,
        },
    ],
    "temple_a_d-15": [
        {
            "name": "Search Key 3",
            "x": 399,
            "y": 263,
        },
    ],
    "temple_b_b-02": [
        {
            "name": "Central Chamber Key 1",
            "x": 71,
            "y": 279,
        },
        {
            "name": "Central Chamber Key 2",
            "x": 247,
            "y": 279,
        },
    ],
    "summit_a_f-07": [
        {
            "name": "2500 M Key",
            "x": 279,
            "y": 39,
        },
    ],
}

LEVEL_CLEARS = {
    "prologue_a_3": {
        "x": 935,
        "y": 110,
    },
    "city_a_end": {
        "x": 240,
        "y": 130,
    },
    "site_a_end_6": {
        "x": 150,
        "y": 130,
    },
    "resort_a_roof07": {
        "x": 5,
        "y": 70,
    },
    "ridge_a_d-10": {
        "x": 130,
        "y": 805,
    },
    "temple_a_e-11": {
        "x": 1035,
        "y": 105,
    },
    "reflection_a_after-01": {
        "x": 160,
        "y": 5,
    },
    "summit_a_g-03": {
        "x": 1825,
        "y": 390,
    },
}

WINGED_GOLDEN = {
    "room_code": "city_a_end",
    "x": 110,
    "y": 90,
}

with Path("data/celeste.json") as f:
    data = json.load(f)

with Path("data/ids.json") as f:
    ids = json.load(f)["location_name_to_id"]


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
    golden_strawberry_room: str = ""


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
        return Route(*self.route, region_index)

    def extended_to_region(self, region_id: str) -> "Route | None":
        return self.extend(RegionIndex(self.back().room_id, region_id))


@dataclass
class Todo:
    route: list[RegionIndex]
    rule: ApRule


with Path("data/CelesteLevelData.json").open() as f:
    level_data = json.load(f)["levels"]

ap_chapters: dict[str, ApChapter] = {}
for chapter_data in level_data:
    if chapter_data["name"].startswith("10"):
        continue

    print(f"Calculating rules for {chapter_data['display_name']}")  # noqa: T201

    rooms = {}
    chapter = ApChapter(rooms=rooms)
    ap_chapters[chapter_data["name"]] = chapter

    # Convert individual room data
    for room_data in chapter_data["rooms"]:
        room = ApRoom(
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
        rooms[room_data["name"]] = room

        if any(
            "Golden Strawberry" in region.entity_rules
            for region in room.regions.values()
        ):
            chapter.golden_strawberry_room = room_data["name"]

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

    if entity == "Golden Strawberry":
        room_id = chapter.golden_strawberry_room

    region, _region_id = next(
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
            map_id = f"{chapter['id']}_{side['id']}_{checkpoint['abbreviation']}"
            canvas_offset = checkpoint["canvas"]["position"]

            for room_id, room in side["rooms"].items():
                if room["checkpointNo"] != checkpoint_idx:
                    continue

                room_offset = room["canvas"]["position"]

                def add_location(entity, img_name, name, ap_name=None, ap_id=None):
                    # ruff: disable[B023] Recapturing the variables every loop is intended
                    map_location = {
                        "map": map_id,
                        "x": room_offset["x"] - canvas_offset["x"] + entity["x"],
                        "y": room_offset["y"] - canvas_offset["y"] + entity["y"],
                    }

                    if ap_name is None:
                        ap_name = name
                    locations_children.append(
                        {
                            "name": name,
                            "access_rules": get_access_rules(
                                chapter, side, room_id, ap_name
                            ),
                            "map_locations": [map_location],
                            "sections": [{}],
                            "chest_unopened_img": f"images/locations/{img_name}.png",
                            "chest_opened_img": (
                                f"images/locations/{img_name}_collected.png"
                            ),
                        }
                    )

                    if ap_id is None:
                        ap_id = ap_name
                    side_name = (
                        f" {side['name']}"
                        if chapter["id"] not in ["prologue", "epilogue", "farewell"]
                        else ""
                    )
                    mappings[ids[f"{chapter['name']}{side_name} - {ap_id}"]] = name
                    # ruff: enable[B023]

                room_code = f"{chapter['id']}_{side['id']}_{room_id}"

                berry_count = len(room["entities"].get("berry", []))
                for entity in room["entities"].get("berry", []):
                    berry_id = f"{chapter['id']}_{room_id}_{entity['id']}"
                    suffix = f" {BERRY_MAPPING[berry_id]}" if berry_count > 1 else ""
                    name = (
                        f"{chapter['name']} {side['name']} [Room {room_id}]"
                        f" Strawberry{suffix}"
                    )
                    add_location(
                        entity,
                        "strawberry",
                        name,
                        f"Strawberry{suffix}",
                        f"Room {room_id} Strawberry{suffix}",
                    )

                for entity in room["entities"].get("golden", []):
                    name = f"{chapter['name']} {side['name']} Golden Strawberry"
                    add_location(entity, "golden_strawberry", name, "Golden Strawberry")

                for entity in room["entities"].get("cassette", []):
                    name = f"{chapter['name']} Cassette"
                    add_location(entity, "cassette", name, "Cassette")

                for entity in room["entities"].get("heart", []):
                    # Skip unreachable heart in final checkpoint of Old Site A
                    if room_code == "site_a_end_s1":
                        continue

                    heart_color = HEART_COLORS[side["id"]]
                    name = f"{chapter['name']} {heart_color.title()} Heart"
                    ap_name = (
                        "Crystal Heart"
                        if side["id"] == "a" and chapter["id"] != "core"
                        else "Level Clear"
                    )
                    add_location(entity, f"{heart_color}_heart", name, ap_name)

                if room_code in LEVEL_CLEARS:
                    entity = LEVEL_CLEARS[room_code]
                    name = f"{chapter['name']} Level Clear"
                    add_location(entity, "clear", name, "Level Clear")

                if WINGED_GOLDEN["room_code"] == room_code:
                    add_location(
                        WINGED_GOLDEN,
                        "winged_golden_strawberry",
                        "Winged Golden Strawberry",
                    )

                for entity in KEYS.get(room_code, []):
                    add_location(entity, "key", entity["name"])

with Path("tracker/locations.json").open("w") as f:
    json.dump(locations, f)

mappings = ",".join(f'[{k}] = "@{v}/"' for k, v in mappings.items())

mappings_path = Path("tracker/scripts/mappings")
mappings_path.mkdir(parents=True, exist_ok=True)

mappings_path /= "locations.lua"
with mappings_path.open("w") as f:
    f.write("LOCATION_MAPPINGS={")
    f.write(mappings)
    f.write("}")
