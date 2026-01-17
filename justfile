PACK_LOCATION := "~/PopTracker/packs/Celeste-OpenWorld-AP-Tracker.zip"

check:
    ruff check
    ruff format --check
    uvx mbake format --check Makefile

build:
    make -rj

build_maps:
    uv run generator/generate_map_images.py

[working-directory: "tracker"]
install: build
    rm -f {{PACK_LOCATION}}
    zip -r {{PACK_LOCATION}} *

