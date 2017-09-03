from django.db import models
from django.contrib.auth.models import User
import uuid


def generate_uuid():
    return str(uuid.uuid4())


# # Create your models here.
# class User(models.Model):
#     username = models.CharField(default="Guest", max_length=80)
#     is_temp = models.BooleanField(default=False)


class Room(models.Model):
    room_password = models.CharField(max_length=40, default='')
    room_name = models.CharField(max_length=40)
    host = models.ForeignKey(User)
    last_used = models.DateTimeField(auto_now=True)


class InRoom(models.Model):
    room = models.ForeignKey('Room')
    user = models.ForeignKey(User)
