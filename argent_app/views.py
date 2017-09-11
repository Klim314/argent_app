from django.shortcuts import render, reverse, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.views import View
from argent_app.models import Room, InRoom
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



# Create your views here.
class Index(View):
    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse("room_manage"))
        return render(request, "argent_app/index.html", {})


class Manage(View):
    """
    View that allows for the viewing, creation and joining of rooms
    """

    def get(self, request):
        rooms = Room.objects.all()
        return render(request, "argent_app/room_manage.html",
                      context={"room_data": [(room.host,
                                              room.room_name,
                                              "placeholder",
                                              room.id,
                                              bool(room.room_password)) for room in rooms]})


class Create(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return render(request, "argent_app/index.html",
                          {"error_message": "Please register an account"})
        else:
            post = request.POST
            room, created = Room.objects.get_or_create(room_name=post['room-name'],
                                                       room_password=post['room-password'],
                                                       host=User.objects.get(id=request.user.id))
            return HttpResponseRedirect(reverse("room_join") + '?room={}'.format(room.id))


class Browse(View):
    def get(self, request):
        if "start" not in request.GET:
            start = 0
        rooms = Room.objects.filter()[start: start + 10]
        return render(request, "argent_app/room_browse.html", {"rooms": rooms})


class Join(View):
    def get(self, request):
        room = Room.objects.get(id=request.GET['room_id'])
        user = request.user
        print(room.host.id, request.user.id)
        # Check if user is already in room
        current_users = [i.user.username for i in InRoom.objects.filter(room=room)]
        if room.host == request.user or InRoom.objects.filter(room=room, user=user).first():
            return HttpResponse(("Welcome user {} to room {}.\n"
                                 "Current users: {}").format(user.username,
                                                             room.room_name,
                                                             current_users))
        # User not in room, check credentials
        if room.room_password and request.GET["password"] != room.room_password:
            return HttpResponse("Invalid password")
        in_room, created = InRoom.objects.get_or_create(room=room,
                                                        user=request.user)
        return HttpResponse(("Welcome user {} to room {}.\n"
                             "Current users: {}").format(user.username,
                                                         room.room_name,
                                                         current_users))



class RoomQuery(View):
    """
    Queries for room information.
    """
    def get(self, request):
        #
        print("USERID", request.user.id)
        print("HOT")
        print(request.GET)
        if "room_id" not in request.GET:
            raise Exception("No id in query get request ")
        room_id = request.GET["room_id"]
        room = Room.objects.get(id=room_id)
        if not room:
            return JsonResponse({"status": False}, status=404)
        elif (room.host == request.user or
              InRoom.objects.filter(user=request.user, room=room).first()):
            return JsonResponse({
                "status": True,
                "passworded": False
                })
        else:
            print("RETURNED")
            return JsonResponse({
                "status": True,
                "passworded": bool(room.room_password)})

class RoomFunctions(View):
    """

    """
    def get(self, request):
        pass
    def kick(self, user, room):
        pass
    def invite(self, user, room):
        pass
