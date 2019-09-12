FROM tarantool/tarantool

ADD .rocks /opt/app
ADD app.lua /opt/app/app.lua
ADD handlers.lua /opt/app/handlers.lua
WORKDIR /opt/app

ENTRYPOINT ["tarantool", "app.lua"]