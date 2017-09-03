from channels import Group
from channels.sessions import channel_session
from argent_app.models import Room
import json


# Connected to websocket.connect
@channel_session
def ws_connect(message):
    print("MESSAGE: ", message.content)
    data = message.content["path"].strip("/").split("/")
    print("DATA: ", data)

    # Check that player is in room
    if data[0] == "room" and data[1] == "join":
        room_id = data[2].strip()

    # Add room to session_store

    message.channel_session["room_id"] = room_id
    print("ROOM ADDED")

    room = Room.objects.get(room_id = room_id)

    print("adding person to room {}".format(room.room_name))
    groupname = "group-" + room.room_id
    print("Groupname: ", groupname)
    Group(groupname).add(message.reply_channel)

    # account for the additional players
    room.current_members += 1
    room.save()

    # Group(groupname).send({
    #   "type": "update_game_state",
    #   "data": rsm.rooms[room_id]
    #   })

@channel_session
def ws_disconnect(message):
    print("leaving room {}".format(message.channel_session["room_id"]))
    Group("group-{}".format(message.channel_session["room_id"])).discard(message.reply_channel)
    print("leaving server")

@channel_session
def ws_recieve(message):
    print("sending_message")
    print("MESSAGE: ", message.content)
    data = json.loads(message.content["text"])
    # Determine message type and dispatch appropriately
    ddict = {
    "update_card": proc.update_card,
    "update_player_color": proc.update_player_color,
    "request_game_state": proc.push_game_state,
    "initial_connect": proc.initial_connect
    }

    ddict[data["type"]](rsm, data, message)

    # # CONVERT THIS TO A DISPATCH DICT
    # # Update single card
    # if data["type"] == "update_card":
    #   rsm.update_card(message.channel_session["room_id"], data["card_number"], data["mark_state"], data["player_color"])
    #   groupname = "group-" + message.channel_session["room_id"]
    #   payload = {
    #   "text": json.dumps({
    #           "type": "update_board_state",
    #           "data": rsm.rooms[message.channel_session["room_id"]]["cards"]
    #           })
    #   }
    #   Group(groupname).send(payload)
    # # Update
    # elif data["type"] == "update":
    #   data = message.content
    #   rsm.update_room(data["room_id"], data["card_index"], data["player_color"])
    # elif data["type"] == "initial_connect":
    #   rsm.add_player_to_room(data["user_id"], data["room_id"]) 
    #   groupname = "group-" + data["room_id"]
    #   payload = {
    #   "text": json.dumps({
    #           "type": "update_add_player",
    #           "player_id": data["user_id"]
    #           })
    #   }
    #   print("SENDING PAYLOAD", payload)
    #   Group(groupname).send(payload)
    # elif data["type"] == "update_player_color":
    #   player_id = data["player_id"]
    #   color, state = data["color"], data["state"]
    #   res = rsm.change_player_color(message.channel_session["room_id"], player_id, color, state)
    #   # Push update if necessary
    #   # if (res == 0):
    #   payload = {
    #   "text": json.dumps({
    #           "type": "update_player_colors",
    #           "player_dict": rsm.rooms[message.channel_session["room_id"]]["players"],
    #           "player_colors": rsm.rooms[message.channel_session["room_id"]]["player_colors"]
    #       })
    #   }
    #   groupname = "group-" + message.channel_session["room_id"]
    #   print("Pushing update_player_colors to: ", groupname)
    #   Group(groupname).send(payload)
        

    # print(rsm.rooms)

