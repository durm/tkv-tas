host = "localhost"
port = 5051
reqLimit = 3

httpd = require("http.server").new(host, port)
log = require('log')
digest = require('digest')

-------------
-- errors
-------------

function methodNotAllowedError(req)
    return errorResponse(req, 405, 'Method not allowed')
end

function badRequestError(req)
    return errorResponse(req, 400, 'Bad request')
end

function notFoundError(req)
    return errorResponse(req, 404, 'Not found')
end

function conflictError(req)
    return errorResponse(req, 409, 'Conflict')
end

function requestLimitError(req)
    return errorResponse(req, 429, 'Request limit error')
end

function errorResponse(req, status, message)
    local resp = req:render({text = req.method..' '..req.path..' '..status..' '..message})
    resp.status = status
    return resp
end

-------------

function handleRequestLimit(req, h)
    local ip_addr = digest.md5(req.peer.host)
    local item = box.space.client:get{ip_addr}

    box.begin()
    local currentTs = os.time()
    if item == nil then
        box.space.client:insert{ip_addr, currentTs, 1}
    else
        local times
        if item[2] == currentTs then
            if item[3] + 1 > reqLimit then
                log.warn("request limit...")
                return requestLimitError(req)
            end
            times = item[3] + 1
        else
            times = 1
        end
        box.space.client:put{ip_addr, currentTs, times}
    end
    box.commit()
    return h(req)
end

function resolveHandler(req)
    log.info("resolve handler for method %s", req.method)
    if req.method == "GET" then
        return getValue(req)
    elseif req.method == "PUT" then
        return putValue(req)
    elseif req.method == "DELETE" then
        return deleteValue(req)
    else
        log.warn("method not allowed %s", req.method)
        return methodNotAllowedError(req)
    end
end

-------------

httpd:route({ path = "/kv/:id" },  function (req) return handleRequestLimit(req, resolveHandler) end)
httpd:route({ path = "/kv" }, function (req) return handleRequestLimit(req, postValue) end)

httpd:start()