ScriptHost:LoadScript("scripts/mappings/items.lua")

Archipelago:AddClearHandler("clear handler", function(slot_data)
	for _, code in pairs(ITEM_MAPPINGS) do
		Tracker:FindObjectForCode(code).Active = false
	end
end)

Archipelago:AddItemHandler("item handler", function(index, item_id, item_name, player)
	local code = ITEM_MAPPINGS[item_id]
	if code then
		Tracker:FindObjectForCode(code).Active = true
	end
end)
