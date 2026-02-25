ScriptHost:LoadScript("scripts/mappings/items.lua")
ScriptHost:LoadScript("scripts/mappings/locations.lua")

Archipelago:AddClearHandler("clear handler", function(slotData)
    setmetatable(slotData, {
        __index = function(_tbl, key)
            logDebug(("Attempting to access non-existent slot data field `%s`"):format(key))
        end
    })

    logDebug("onClear handler called. If verbose debugging enabled, dumping slot data below.")
    logDebugVerbose(dumpTable(slotData))
    -- Slot data reference can be found at: https://github.com/PoryGoneDev/Celeste-Archipelago-Open-World/blob/main/Source/ArchipelagoManager.cs
    -- A sample can found at: ~/docs/tracker/SLOT_DATA.sample

    -- Reset locations
    for _, locationCode in pairs(LOCATION_MAPPINGS) do
        logDebugVerbose(string.format('Resetting location %s', locationCode))

        local obj = Tracker:FindObjectForCode(locationCode)
        logDebugVerbose(tostring(obj))

        obj.AvailableChestCount = obj.ChestCount
    end

    logDebug("onClear: Mapped locations reset successfully.")

    -- Reset items
    for _, itemCode in pairs(ITEM_MAPPINGS) do
        Tracker:FindObjectForCode(itemCode).Active = false
    end

    logDebug("onClear: Mapped items reset successfully.")

    local cumulativeTrackerItems = {"berries_obtained_total", "raspberries_obtained_total", "hearts_obtained_total",
                                    "cassettes_obtained_total"}
    for _, trackerCode in ipairs(cumulativeTrackerItems) do
        Tracker:FindObjectForCode(trackerCode).AcquiredCount = 0
    end

    logDebug("onClear: Cumulative tracker items reset successfully.")

    -- Reset settings

    -- Deathlink is special because of amnesty, so we merge two settings into one icon here.
    local deathLinkCount = 0
    if (slotData["death_link"] or 0) ~= 0 then
        deathLinkCount = slotData["death_link_amnesty"] or 0
    end
    Tracker:FindObjectForCode("death_link").AcquiredCount = deathLinkCount

    Tracker:FindObjectForCode("goal").CurrentStage = _mapSlotGoalAreaCodeToGoalObjectIndex(slotData["goal_area"])

    local settingKeys = {"trap_link", "strawberries_required", "lock_goal_area", "binosanity", "carsanity",
                         "checkpointsanity", "gemsanity", "keysanity", "roomsanity", "include_goldens", "include_core",
                         "include_farewell", "include_b_sides", "include_c_sides"}

    for _, settingKey in ipairs(settingKeys) do
        local obj = Tracker:FindObjectForCode(settingKey)
        if obj.Type == "toggle" then
            obj.Active = slotData[settingKey]
        elseif obj.Type == "progressive" then
            obj.CurrentStage = slotData[settingKey]
        elseif obj.Type == "consumable" then
            obj.AcquiredCount = slotData[settingKey]
        else
            logDebugVerbose(string.format("onClear: unknown setting item type %s for code %s", obj.Type, settingKey))
        end
    end

    logDebug("onClear: Settings and goals reset completed.")
end)

Archipelago:AddItemHandler("item handler", function(index, item_id, item_name, player)
    -- TODO(matthewjaykoster) Update to handle progressive items/items with counts
    local code = ITEM_MAPPINGS[item_id]
    if code then
        Tracker:FindObjectForCode(code).Active = true
    end
end)

Archipelago:AddLocationHandler("location handler", function(location_id, location_name)
    local code = LOCATION_MAPPINGS[location_id]
    if code then
        Tracker:FindObjectForCode(code).AvailableChestCount = 0
    end
end)

--- Maps a level code (e.g. 10c) to its name code (e.g. farewell_golden).
---@param levelCode string
function _mapSlotGoalAreaCodeToGoalObjectIndex(levelCode)
    local goalAreaCodeToGoalIndex = setmetatable({
        ["7a"] = 0, -- the_summit_a
        ["7b"] = 1, -- the_summit_b
        ["7c"] = 1, -- the_summit_c
        ["9a"] = 1, -- core_a
        ["9b"] = 1, -- core_b
        ["9c"] = 1, -- core_c
        ["10a"] = 1, -- empty_space
        ["10b"] = 1, -- farewell
        ["10c"] = 1 -- farewell_golden
    }, {
        __index = function(_tbl, key)
            logDebug(string.format(
                'Error: Found invalid Goal Area level code (%s) when mapping to name code. Defaulting to Summit A.'),
                levelCode)
            return 0 -- return "the_summit_a"
        end
    })

    return goalAreaCodeToGoalIndex[levelCode]
end
