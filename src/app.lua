#!/usr/bin/env tarantool

box.cfg{
    listen = 5050
}

box.once("kv_space", function() 
    space = box.schema.space.create("kv")
    space:create_index('primary', { type = 'tree', parts = { 1, 'string' } })
end)

require 'handlers'