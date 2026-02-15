ScriptHost:LoadScript("scripts/mappings/items.lua")
ScriptHost:LoadScript("scripts/mappings/locations.lua")

CUR_INDEX = -1
SLOT_DATA = nil

Archipelago:AddClearHandler("clear handler", function(slot_data)

    logDebug("onClear handler called. If verbose debugging enabled, dumping slot data below.")
    logDebugVerbose(dumpTable(slot_data))
    -- Slot data reference can be found at: https://github.com/PoryGoneDev/Celeste-Archipelago-Open-World/blob/main/Source/ArchipelagoManager.cs
    -- A sample can found at: ./SLOT_DATA.sample

    SLOT_DATA = slot_data
    CUR_INDEX = -1

    -- reset locations
    for _, location in pairs(LOCATION_MAPPINGS) do
        if location then
            local obj = Tracker:FindObjectForCode(location)
            if obj then
                logDebugVerbose(string.format('Resetting location %s', location))
                logDebugVerbose(tostring(obj))
                if location:sub(1, 1) == "@" then
                    obj.AvailableChestCount = obj.ChestCount
                else
                    obj.Active = false
                end
            end
        end
    end

    logDebug("onClear: Locations reset successfully.")

    -- reset items
    for _, item in pairs(ITEM_MAPPINGS) do
        if item[1] and item[2] then
            local obj = Tracker:FindObjectForCode(item[1])
            if obj then
                if item[2] == "toggle" then
                    obj.Active = false
                elseif item[2] == "progressive" then
                    obj.CurrentStage = 0
                    obj.Active = false
                elseif item[2] == "consumable" then
                    obj.AcquiredCount = 0
                else
                    logDebugVerbose(string.format("onClear: unknown item type %s for code %s", item[2], item[1]))
                end
            else
                logDebugVerbose(string.format("onClear: could not find object for code %s", item[1]))
            end
        end
    end

    logDebug("onClear: Items reset successfully.")

    PLAYER_ID = Archipelago.PlayerNumber or -1
    TEAM_NUMBER = Archipelago.TeamNumber or 0

    logDebug("onClear: Player ID and Team Number reset successfully.")

    -- Settings: Game Options
    if slot_data["death_link"] ~= nil and slot_data["death_link"] ~= 0 and slot_data["death_link_amnesty"] ~= nil then
        Tracker:FindObjectForCode("death_link").AcquiredCount = tonumber(slot_data["death_link_amnesty"])
    else
        Tracker:FindObjectForCode("death_link").AcquiredCount = 0
    end
    if slot_data["trap_link"] ~= nil then
        Tracker:FindObjectForCode("trap_link").Active = tonumber(slot_data["trap_link"])
    end

    -- Settings: Goal Options
    if slot_data["strawberries_required"] ~= nil then
        Tracker:FindObjectForCode("berries_required").AcquiredCount = tonumber(slot_data["strawberries_required"])
    end
    if slot_data["lock_goal_area"] ~= nil then
        Tracker:FindObjectForCode("lock_goal_area").Active = tonumber(slot_data["lock_goal_area"])
    end
    if slot_data["goal_area_checkpointsanity"] ~= nil then
        Tracker:FindObjectForCode("goal_area_checkpointsanity").Active = tonumber(
            slot_data["goal_area_checkpointsanity"])
    end
    if slot_data["goal_area"] then
        Tracker:FindObjectForCode("goal").CurrentStage = _mapSlotGoalAreaCodeToGoalObjectIndex(slot_data["goal_area"])
    end

    -- Settings: Location Options/-sanities
    if slot_data["binosanity"] ~= nil then
        Tracker:FindObjectForCode("binosanity").Active = tonumber(slot_data["binosanity"])
    end
    if slot_data["carsanity"] ~= nil then
        Tracker:FindObjectForCode("carsanity").Active = tonumber(slot_data["carsanity"])
    end
    if slot_data["checkpointsanity"] ~= nil then
        Tracker:FindObjectForCode("checkpointsanity").Active = tonumber(slot_data["checkpointsanity"])
    end
    if slot_data["gemsanity"] ~= nil then
        Tracker:FindObjectForCode("gemsanity").Active = tonumber(slot_data["gemsanity"])
    end
    if slot_data["keysanity"] ~= nil then
        Tracker:FindObjectForCode("keysanity").Active = tonumber(slot_data["keysanity"])
    end
    if slot_data["roomsanity"] ~= nil then
        Tracker:FindObjectForCode("roomsanity").Active = tonumber(slot_data["roomsanity"])
    end

    -- Settings: Location Options/checks
    if slot_data["include_goldens"] ~= nil then
        Tracker:FindObjectForCode("include_goldens").Active = tonumber(slot_data["include_goldens"])
    end
    if slot_data["include_core"] ~= nil then
        Tracker:FindObjectForCode("include_core").Active = tonumber(slot_data["include_core"])
    end
    if slot_data["include_farewell"] ~= nil then
        -- 0 == "None", 1 == "Empty Space", 2 == "Farewell"
        Tracker:FindObjectForCode("include_farewell").CurrentStage = tonumber(slot_data["include_farewell"])
    end
    if slot_data["include_b_sides"] ~= nil then
        Tracker:FindObjectForCode("include_b_sides").Active = tonumber(slot_data["include_b_sides"])
    end
    if slot_data["include_c_sides"] ~= nil then
        Tracker:FindObjectForCode("include_c_sides").Active = tonumber(slot_data["include_c_sides"])
    end

    logDebug("onClear: Settings and goals reset completed.")
end)

Archipelago:AddItemHandler("item handler", function(index, item_id, item_name, player)
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
---@param level_code string
function _mapSlotGoalAreaCodeToGoalObjectIndex(level_code)
    if level_code == "7a" then
        return 0
        -- return "the_summit_a"
    elseif level_code == "7b" then
        return 1
        -- return "the_summit_b"
    elseif level_code == "7c" then
        return 2
        -- return "the_summit_c"
    elseif level_code == "9a" then
        return 3
        -- return "core_a"
    elseif level_code == "9b" then
        return 4
        -- return "core_b"
    elseif level_code == "9c" then
        return 5
        -- return "core_c"
    elseif level_code == "10a" then
        return 6
        -- return "empty_space"
    elseif level_code == "10b" then
        return 7
        -- return "farewell"
    elseif level_code == "10c" then
        return 8
        -- return "farewell_golden"
    else
        logDebug(string.format(
            'Error: Found invalid Goal Area level code (%s) when mapping to name code. Defaulting to Summit A'),
            level_code);
        return 0
        -- return "the_summit_a"
    end
end
