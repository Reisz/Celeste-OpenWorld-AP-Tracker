"""Generates auto-tracker mappings for items in `interactables.json`."""

import json
from pathlib import Path

with Path("data/ids.json").open() as f:
    ids = json.load(f)["item_name_to_id"]

with Path("tracker/items/interactables.json").open() as f:
    interactables = json.load(f)

mappings = {}
for interactable in interactables:
    mappings[ids[interactable["name"]]] = interactable["codes"]

mappings_path = Path("tracker/scripts/mappings")
mappings_path.mkdir(parents=True, exist_ok=True)

mappings_path /= "items.lua"
with mappings_path.open("w") as f:
    f.write("ITEM_MAPPINGS={")
    f.write(",".join(f'[{k}] = "{v}"' for k, v in mappings.items()))
    f.write("}")
