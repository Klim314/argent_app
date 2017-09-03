# In routing.py
from channels.routing import route
from argent_app.consumers import ws_connect, ws_disconnect, ws_recieve
channel_routing = [
    route("websocket.connect", ws_connect),
    route("websocket.disconnect", ws_disconnect),
    route("websocket.message", ws_recieve),
]