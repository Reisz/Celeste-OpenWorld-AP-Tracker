PACK_LOCATION := "~/PopTracker/packs/Celeste-OpenWorld-AP-Tracker.zip"
ARCHIPELAGO_VERSION := "0.6.5"
CELESTE_MOD_VERSION := "1.0.7"
JQ_FORMAT_ARGS := "--indent 4"

# Check formatting and lint files in repository
check:
    uv run ruff check
    uv run ruff format --check
    fd -e json -x sh -c 'jq {{ JQ_FORMAT_ARGS }} . {} | cmp {}'
    just --fmt --unstable --check
    uv run rumdl check

# Download everything needed to build the pack
download:
    mkdir -p data
    curl -ZL --output-dir data \
        "https://github.com/berrycamp/berrycamp.github.io/archive/refs/heads/dev.zip" -o berrycamp.zip \
        -O "https://raw.githubusercontent.com/ArchipelagoMW/Archipelago/refs/tags/{{ ARCHIPELAGO_VERSION }}/worlds/celeste_open_world/data/CelesteLevelData.json"
    unzip -jo data/berrycamp.zip berrycamp.github.io-dev/data/celeste.json -d data
    curl "https://archipelago.gg/datapackage" | jq '.games."Celeste (Open World)" | pick(.item_name_to_id, .location_name_to_id)' > data/ids.json

    mkdir -p tracker/images/items
    jq -r '.[].img | "https://github.com/PoryGoneDev/Celeste-Archipelago-Open-World/blob/v{{ CELESTE_MOD_VERSION }}/Graphics/Atlases/Journal/" + split("/")[-1] + "?raw=true"' tracker/items/interactables.json \
        | xargs curl -ZL --output-dir tracker/images/items --remote-name-all 

# Run the scripts to generate the pack
build:
    uv run generator/generate_maps.py
    uv run generator/generate_locations.py
    uv run generator/generate_ap_item_mappings.py
    # Map generation is slow and unlikely to change. Only run if needed.
    test -d tracker/images/maps || uv run generator/generate_map_images.py

# Build the pack and install to local PopTracker
[working-directory("tracker")]
install: build
    zip -rFS {{ PACK_LOCATION }} *
