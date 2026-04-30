"""Generates auto-tracker mappings for items in `interactables.json`."""

import json
from pathlib import Path

with Path("data/ids.json").open() as f:
    ids = json.load(f)["item_name_to_id"]

ITEM_TYPES = ["interactables", "keys", "checkpoints"]

mappings = {}

for item_type in ITEM_TYPES:
    with Path(f"tracker/items/{item_type}.json").open() as f:
        items = json.load(f)

    for item in items:
        mappings[ids[item["name"]]] = item["codes"]

mappings_path = Path("tracker/scripts/mappings")
mappings_path.mkdir(parents=True, exist_ok=True)

mappings_path /= "items.lua"
with mappings_path.open("w") as f:
    f.write("return {")
    f.write(",".join(f'[{k}] = "{v}"' for k, v in mappings.items()))
    f.write("}")
