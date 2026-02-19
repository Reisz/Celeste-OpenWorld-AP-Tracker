ScriptHost:LoadScript("scripts/mappings/items.lua")
ScriptHost:LoadScript("scripts/mappings/locations.lua")

CUR_INDEX = -1
SLOT_DATA = nil

Archipelago:AddClearHandler("clear handler", function(slotData)

    logDebug("onClear handler called. If verbose debugging enabled, dumping slot data below.")
    logDebugVerbose(dumpTable(slotData))
    -- Slot data reference can be found at: https://github.com/PoryGoneDev/Celeste-Archipelago-Open-World/blob/main/Source/ArchipelagoManager.cs
    -- A sample can found at: ~/docs/tracker/SLOT_DATA.sample

    SLOT_DATA = slotData
    CUR_INDEX = -1

    -- Reset Locations
    for _, location in pairs(LOCATION_MAPPINGS) do
        _resetLocation(location)
    end

    logDebug("onClear: Locations reset successfully.")

    -- Reset Items
    for _, item in pairs(ITEM_MAPPINGS) do
        _resetItem(item)
    end

    -- Items: cumulative trackers
    _resetCumulativeTracker("berries_obtained_total")
    _resetCumulativeTracker("raspberries_obtained_total")
    _resetCumulativeTracker("hearts_obtained_total")
    _resetCumulativeTracker("cassettes_obtained_total")

    logDebug("onClear: Items reset successfully.")

    PLAYER_ID = Archipelago.PlayerNumber or -1
    TEAM_NUMBER = Archipelago.TeamNumber or 0

    logDebug("onClear: Player ID and Team Number reset successfully.")

    -- Settings: Game Options
    if slotData["death_link"] ~= nil and slotData["death_link"] ~= 0 and slotData["death_link_amnesty"] ~= nil then
        Tracker:FindObjectForCode("death_link").AcquiredCount = tonumber(slotData["death_link_amnesty"])
    else
        Tracker:FindObjectForCode("death_link").AcquiredCount = 0
    end

    _resetToggleSettingFromSlotData(slotData, "trap_link", "trap_link")

    -- Settings: Goal Options
    _resetCountSettingFromSlotData(slotData, "strawberries_required", "berries_required")
    _resetToggleSettingFromSlotData(slotData, "lock_goal_area", "lock_goal_area")
    _resetToggleSettingFromSlotData(slotData, "goal_area_checkpointsanity", "goal_area_checkpointsanity")

    if slotData["goal_area"] then
        Tracker:FindObjectForCode("goal").CurrentStage = _mapSlotGoalAreaCodeToGoalObjectIndex(slotData["goal_area"])
    end

    -- Settings: Location Options/-sanities
    _resetToggleSettingFromSlotData(slotData, "binosanity", "binosanity")
    _resetToggleSettingFromSlotData(slotData, "carsanity", "carsanity")
    _resetToggleSettingFromSlotData(slotData, "checkpointsanity", "checkpointsanity")
    _resetToggleSettingFromSlotData(slotData, "gemsanity", "gemsanity")
    _resetToggleSettingFromSlotData(slotData, "keysanity", "keysanity")
    _resetToggleSettingFromSlotData(slotData, "roomsanity", "roomsanity")

    -- Settings: Location Options/checks
    _resetToggleSettingFromSlotData(slotData, "include_goldens", "include_goldens")
    _resetToggleSettingFromSlotData(slotData, "include_core", "include_core")
    _resetProgressiveSettingFromSlotData(slotData, "include_farewell", "include_farewell") -- 0 == "None", 1 == "Empty Space", 2 == "Farewell"
    _resetToggleSettingFromSlotData(slotData, "include_b_sides", "include_b_sides")
    _resetToggleSettingFromSlotData(slotData, "include_c_sides", "include_c_sides")

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
            'Error: Found invalid Goal Area level code (%s) when mapping to name code. Defaulting to Summit A'),
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
    if itemCode then
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
end

--- Resets location data to a default state from its mapping code.
--- @param locationCode string
function _resetLocation(locationCode)
    if locationCode then
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
end

--- Resets a count-based "setting item" to its slot data state.
--- @param slotData table
--- @param slotDataKey string
--- @param settingTrackerKey string
function _resetCountSettingFromSlotData(slotData, slotDataKey, settingTrackerKey)
    if slotData[slotDataKey] ~= nil then
        Tracker:FindObjectForCode(settingTrackerKey).AcquiredCount = tonumber(slotData[slotDataKey])
    end
end

--- Resets a toggleable "setting item" to its slot data state.
--- @param slotData table
--- @param slotDataKey string
--- @param settingTrackerKey string
function _resetProgressiveSettingFromSlotData(slotData, slotDataKey, settingTrackerKey)
    if slotData[slotDataKey] ~= nil then
        Tracker:FindObjectForCode(settingTrackerKey).CurrentStage = tonumber(slotData[slotDataKey])
    end
end

--- Resets a toggleable "setting item" to its slot data state.
--- @param slotData table
--- @param slotDataKey string
--- @param settingTrackerKey string
function _resetToggleSettingFromSlotData(slotData, slotDataKey, settingTrackerKey)
    if slotData[slotDataKey] ~= nil then
        Tracker:FindObjectForCode(settingTrackerKey).Active = tonumber(slotData[slotDataKey])
    end
end
