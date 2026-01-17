import json
import pathlib

ids = json.load(open("data/ids.json"))["item_name_to_id"]
mappings = {}

interactables = json.load(open("tracker/items/interactables.json"))
for interactable in interactables:
    mappings[ids[interactable["name"]]] = interactable["codes"]


mappings = ",".join(f'[{k}] = "{v}"' for k, v in mappings.items())

pathlib.Path("tracker/scripts/mappings").mkdir(parents=True, exist_ok=True)
f = open("tracker/scripts/mappings/items.lua", "w")
f.write("ITEM_MAPPINGS={")
f.write(mappings)
f.write("}")
