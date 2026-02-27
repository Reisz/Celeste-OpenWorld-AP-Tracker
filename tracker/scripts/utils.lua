-- Writes a message to console if debug logging is enabled.
function logDebug(message)
    if ENABLE_DEBUG_LOG then
        print(message)
    end
end

-- Writes a message to console if verbose debug logging is enabled.
function logDebugVerbose(message)
    if ENABLE_DEBUG_LOG_VERBOSE then
        print(message)
    end
end

-- from https://stackoverflow.com/questions/9168058/how-to-dump-a-table-to-console
-- Dumps a table in a readable string
function dumpTable(o, depth)
    if depth == nil then
        depth = 0
    end
    if type(o) == 'table' then
        local tabs = ('\t'):rep(depth)
        local s = '{\n'
        for k, v in pairs(o) do
            if type(k) == 'string' then
                k = '"' .. k .. '"'
            end
            s = s .. tabs .. '\t[' .. tostring(k) .. '] = ' .. dumpTable(v, depth + 1) .. ',\n'
        end
        return s .. tabs .. '}'
    elseif type(o) == 'string' then
        return '"' .. o .. '"'
    else
        return tostring(o)
    end
end
