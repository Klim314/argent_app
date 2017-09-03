from django.shortcuts import render, reverse, HttpResponseRedirect, HttpResponse
from django.views import View
from argent_app.models import Room, InRoom
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



# Create your views here.
class Index(View):
    def get(self, request):
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
                                              room.id) for room in rooms]})


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
        room, created = Room.objects.get_or_create(id=request.GET['room_id'])
        user = User.objects.get(id=request.user.id)
        print(room.host.id, request.user.id)
        current_users = [i.user.username for i in InRoom.objects.filter(room=room)]
        if room.host.id == request.user.id or InRoom.objects.filter(room=room, user=user):
            return HttpResponse(("Welcome user {} to room {}.\n"
                                 "Current users: {}").format(user.username,
                                                             room.room_name,
                                                             current_users))
