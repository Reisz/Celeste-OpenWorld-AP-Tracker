PACK_LOCATION := "~/PopTracker/packs/Celeste-OpenWorld-AP-Tracker.zip"

check:
    ruff check
    ruff format --check

build:
    uv run generator/generate_maps.py

build_maps:
    uv run generator/generate_map_images.py

[working-directory: "tracker"]
install: build
    rm -f {{PACK_LOCATION}}
    zip -r {{PACK_LOCATION}} *

