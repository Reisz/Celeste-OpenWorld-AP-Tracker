ARCHIPELAGO_VERSION := 0.6.5
MOD_VERSION := 1.0.7

LOCATION_DATA := tracker/locations.json \
	tracker/scripts/mappings/locations.lua

MAP_DATA := tracker/maps/maps.json \
	tracker/layouts/maps.json

AP_MAPPINGS := tracker/scripts/mappings/items.lua

INCLUDES := data/maps.d data/items.d

GENERATORS := $(wildcard generator/*.py)
GENERATOR_DEPS := $(patsubst generator/%.py,data/%.py.d,$(GENERATORS))

.PHONY: Makefile all included clean clean-all

all: $(LOCATION_DATA) $(MAP_DATA) $(AP_MAPPINGS) included

ifeq (,$(filter clean%,$(MAKECMDGOALS))) # Skip includes for clean* targets
include $(GENERATOR_DEPS) $(INCLUDES)
endif

included: $(MAPS) $(ITEMS)

# Clean generated data
clean:
	rm -f $(LOCATION_DATA) $(MAP_DATA) $(INCLUDES) $(GENERATOR_DEPS) $(AP_MAPPINGS)
	rm -rf tracker/images/maps

# Clean generated and downloaded data
clean-all: clean
	rm -rf data
	rm -rf tracker/images/items

# Generators
# See <https://stackoverflow.com/a/47951465>
.INTERMEDIATE: location_data map_data
$(LOCATION_DATA): location_data
$(MAP_DATA): map_data

location_data: generator/generate_locations.py
	uv run $<

map_data: generator/generate_maps.py
	uv run $<

tracker/images/maps/%.png: generator/generate_map_image.py
	uv run $< $@

tracker/scripts/mappings/items.lua: generator/generate_ap_item_mappings.py
	uv run $<

# Download images
tracker/images/items/%.png:
	@mkdir -p $(@D)
	curl -sL "https://github.com/PoryGoneDev/Celeste-Archipelago-Open-World/blob/v$(MOD_VERSION)/Graphics/Atlases/Journal/$(@F)?raw=true" -o $@

# Download data
data/celeste.json: data/berrycamp.zip
	@mkdir -p $(@D)
	unzip -qjo $< berrycamp.github.io-dev/$@ -d $(@D)
	@touch $@ # Apply new timestamp for make

data/berrycamp.zip:
	@mkdir -p $(@D)
	curl -sL "https://github.com/berrycamp/berrycamp.github.io/archive/refs/heads/dev.zip" -o $@

data/CelesteLevelData.json: data/berrycamp.zip
	@mkdir -p $(@D)
	curl -s "https://raw.githubusercontent.com/ArchipelagoMW/Archipelago/refs/tags/$(ARCHIPELAGO_VERSION)/worlds/celeste_open_world/data/CelesteLevelData.json" -o $@

data/ids.json:
	@mkdir -p $(@D)
	curl -s "https://archipelago.gg/datapackage" | jq '.games."Celeste (Open World)" | pick(.item_name_to_id, .location_name_to_id)' > $@

# Dependencies
data/%.py.d: generator/%.py
	@mkdir -p $(@D)
	rg -o "data/[^\"']*" $< | xargs echo $<: > $@

data/items.d: tracker/items/interactables.json
	@mkdir -p $(@D)
	jq -r '"ITEMS := " + (["tracker/" + .[].img] | join(" "))' $< > $@

data/maps.d: scripts/list_map_image_paths.py data/celeste.json
	@mkdir -p $(@D)
	uv run $< | xargs echo "MAPS :=" > $@
