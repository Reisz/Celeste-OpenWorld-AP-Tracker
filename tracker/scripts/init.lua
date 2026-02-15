Tracker:AddMaps("maps/maps.json")

-- Tracked items
Tracker:AddItems("items/checkpoints.json")
Tracker:AddItems("items/gems.json")
Tracker:AddItems("items/interactables.json")
Tracker:AddItems("items/keys.json")
Tracker:AddItems("items/rooms.json")
Tracker:AddItems("items/traps.json")

-- Layout labels
Tracker:AddItems("items/labels.json")

-- Settings and Goals (often from Slot Data, though not always)
Tracker:AddItems("items/settings_game.json")
Tracker:AddItems("items/settings_goals.json")
Tracker:AddItems("items/settings_locations.json")
Tracker:AddItems("items/settings_totals.json")

-- Pack UI Layout
Tracker:AddLayouts("layouts/maps.json")
Tracker:AddLayouts("layouts/items_layout.json")
Tracker:AddLayouts("layouts/slot_settings_layout.json")
Tracker:AddLayouts("layouts/tracker.json")

-- Pack Lua scripts
ENABLE_DEBUG_LOG = true
ENABLE_DEBUG_LOG_VERBOSE = true

ScriptHost:LoadScript("scripts/utils.lua")
ScriptHost:LoadScript("scripts/archipelago.lua")
