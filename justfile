PACK_LOCATION := "~/PopTracker/packs/Celeste-OpenWorld-AP-Tracker.zip"

JQ_FORMAT_ARGS := "--indent 4"

check:
    uvx ruff@0.15 check
    uvx ruff@0.15 format --check
    fd -e json -x sh -c 'jq {{ JQ_FORMAT_ARGS }} . {} | cmp {}'
    uvx mbake@1.4.5 format --check Makefile

build:
    make -rj

build_maps:
    uv run generator/generate_map_images.py

[working-directory: "tracker"]
install: build
    zip -rFS {{PACK_LOCATION}} *

