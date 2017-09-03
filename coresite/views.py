from django.shortcuts import render, reverse, HttpResponseRedirect, HttpResponse
from django.views import View
from argent_app.models import Room, InRoom
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class Register(View):
    def post(self, request):
        print(request.POST)
        username, password = request.POST["username"], request.POST["password1"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("room_manage"))
        else:
            # if user does not exist, create
            if User.objects.filter(username=username).exists():
                return HttpResponseRedirect(reverse("register"),
                                            context={"user_exists": True})
            else:
                user = User.objects.create_user(username, password=password)
                login(request, user)
                return HttpResponseRedirect(reverse("room_manage"))

    def get(self, request):
        return render(request, "registration/register.html", {"form": UserCreationForm()})
