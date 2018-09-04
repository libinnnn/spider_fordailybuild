package.cpath = '/sbin/redis_cli_plugin/?.so;'..package.cpath
package.path = '/sbin/redis_cli_plugin/?.lua;'..package.path

local pb = require "pb"
local protoc = require "protoc"

os.execute('find /data/protos/ -name "*.proto" | sed "s/\\/data\\/protos\\///g" > .redis-cli-plugin')

file = io.open('.redis-cli-plugin')
for l in file:lines() do
    print('loading:', l)
    assert(protoc:loadfile(l))
end

function convert_cmd(cmds)
    if cmds[1] ~= 'proto' then
        return cmds
    end
    for i, v in ipairs(cmds) do
        cmds[i] = cmds[i + 1]
    end
    if cmds[1] == 'useproto' then
        pkg_name = cmds[2]
        msg_name = cmds[3]
        for i, v in ipairs(cmds) do
            cmds[i] = cmds[i + 3]
        end
        return convert_cmd(cmds)
    elseif cmds[1] == 'set' or cmds[1] == 'publish' or cmds[1] == 'hset' then
        local n = #cmds
        local foo = load('obj = '..cmds[n])
        local succ, reason = pcall(foo)
        if not succ then
            print('obj syntax error: '..reason)
            return {}
        end
        cmds[n] = pb.encode(pkg_name..'.'..msg_name, obj)
        if cmds[n] == nil then
            print('encode error')
            return {}
        end
    end
    return cmds
end

function convert_result(result)
    if pkg_name == nil or msg_name == nil then
        return
    end

    local obj = pb.decode(pkg_name..'.'..msg_name, result)
    if obj == nil then return end

    local res = require("serpent").block(obj)
    local ret = '---begin---\n'..res..'\n---end---\n'
    return ret
end

print('protobuf-plugin load success')
