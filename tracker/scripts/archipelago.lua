ScriptHost:LoadScript("scripts/mappings/items.lua")
ScriptHost:LoadScript("scripts/mappings/locations.lua")

Archipelago:AddClearHandler("clear handler", function(slotData)
    setmetatable(slotData, {
        __index = function(_tbl, key)
            print(("Attempting to access non-existent slot data field `%s`"):format(key))
        end
    })

    logDebug("onClear handler called. If verbose debugging enabled, dumping slot data below.")
    logDebugVerbose(dumpTable(slotData))
    -- Slot data reference can be found at: https://github.com/PoryGoneDev/Celeste-Archipelago-Open-World/blob/main/Source/ArchipelagoManager.cs
    -- A sample can found at: ~/docs/tracker/SLOT_DATA.sample

    -- Reset locations
    for _, location in pairs(LOCATION_MAPPINGS) do
        _resetLocation(location)
    end

    logDebug("onClear: Locations reset successfully.")

    -- Reset items
    for _, item in pairs(ITEM_MAPPINGS) do
        _resetItem(item)
    end

    logDebug("onClear: Items reset successfully.")

    local cumulativeTrackerItems = {"berries_obtained_total", "raspberries_obtained_total", "hearts_obtained_total",
                                    "cassettes_obtained_total"}
    for _, item in ipairs(cumulativeTrackerItems) do
        _resetCumulativeTracker(item)
    end

    logDebug("onClear: Cumulative trackers reset successfully.")

    -- Reset settings

    -- Deathlink is special because of amnesty, so we merge two settings into one icon here.
    local deathLinkCount = slotData["death_link"] ~= 0 and slotData["death_link_amnesty"] or 0
    Tracker:FindObjectForCode("death_link").AcquiredCount = deathLinkCount

    Tracker:FindObjectForCode("goal").CurrentStage = _mapSlotGoalAreaCodeToGoalObjectIndex(slotData["goal_area"])

    local settingKeys = {"trap_link", "strawberries_required", "lock_goal_area", "binosanity", "carsanity",
                         "checkpointsanity", "gemsanity", "keysanity", "roomsanity", "include_goldens", "include_core",
                         "include_farewell", "include_b_sides", "include_c_sides"}

    for _, settingKey in ipairs(settingKeys) do
        _setSettingFromSlotData(slotData, settingKey)
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
    if levelCode == "7a" then
        return 0
        -- return "the_summit_a"
    elseif levelCode == "7b" then
        return 1
        -- return "the_summit_b"
    elseif levelCode == "7c" then
        return 2
        -- return "the_summit_c"
    elseif levelCode == "9a" then
        return 3
        -- return "core_a"
    elseif levelCode == "9b" then
        return 4
        -- return "core_b"
    elseif levelCode == "9c" then
        return 5
        -- return "core_c"
    elseif levelCode == "10a" then
        return 6
        -- return "empty_space"
    elseif levelCode == "10b" then
        return 7
        -- return "farewell"
    elseif levelCode == "10c" then
        return 8
        -- return "farewell_golden"
    else
        logDebug(string.format(
            'Error: Found invalid Goal Area level code (%s) when mapping to name code. Defaulting to Summit A.'),
            levelCode);
        return 0
        -- return "the_summit_a"
    end
end

--- Resets a cumulative tracker item to its default state
--- @param itemCode string
function _resetCumulativeTracker(itemCode)
    local cumulativeTracker = Tracker:FindObjectForCode(itemCode)
    if cumulativeTracker ~= nil then
        cumulativeTracker.AcquiredCount = 0
    else
        logDebugVerbose(string.format("onClear: Failed to find cumulative tracker object for code %s", itemCode))
    end
end

--- Resets item data to a default state from its mapping code.
--- @param itemCode string
function _resetItem(itemCode)
    local obj = Tracker:FindObjectForCode(itemCode)
    if obj ~= nil then
        if obj.Type == "toggle" then
            obj.Active = false
        elseif obj.Type == "progressive" then
            obj.CurrentStage = 0
            obj.Active = false
        elseif obj.Type == "consumable" then
            obj.AcquiredCount = 0
        else
            logDebugVerbose(string.format("onClear: unknown item type %s for code %s", obj.Type, itemCode))
        end
    else
        logDebugVerbose(string.format("onClear: could not find object for code %s", itemCode))
    end
end

--- Resets location data to a default state from its mapping code.
--- @param locationCode string
function _resetLocation(locationCode)
    local obj = Tracker:FindObjectForCode(locationCode)
    if obj ~= nil then
        logDebugVerbose(string.format('Resetting location %s', locationCode))
        logDebugVerbose(tostring(obj))
        if locationCode:sub(1, 1) == "@" then
            obj.AvailableChestCount = obj.ChestCount
        else
            obj.Active = false
        end
    end
end

--- Resets a "setting item" from its related slot data state.
--- @param slotData table
--- @param slotDataKey string
--- @param settingTrackerKey string
function _setSettingFromSlotData(slotData, slotDataKey)
    local obj = Tracker:FindObjectForCode(slotDataKey)
    if obj ~= nil then
        if obj.Type == "toggle" then
            obj.Active = slotData[slotDataKey]
        elseif obj.Type == "progressive" then
            obj.CurrentStage = slotData[slotDataKey]
        elseif obj.Type == "consumable" then
            obj.AcquiredCount = slotData[slotDataKey]
        else
            logDebugVerbose(string.format("onClear: unknown setting item type %s for code %s", obj.Type, slotDataKey))
        end
    else
        logDebugVerbose(string.format("onClear: could not find setting tracker object for code %s", slotDataKey))
    end
end
