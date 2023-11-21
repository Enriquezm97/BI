from channels.routing import ProtocolTypeRouter, URLRouter






application = ProtocolTypeRouter({
    #'websocket': AuthMiddlewareStack(URLRouter([re_path(pipe_ws_endpoint_name(), MessageConsumer if OLDER_CHANNELS else MessageConsumer.as_asgi()),])),
    ##'http': AuthMiddlewareStack(URLRouter(http_routes)),
})