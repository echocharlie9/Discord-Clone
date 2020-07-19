from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model as user_model
User = user_model()
from apps.lobby.main.models import Lobby

class Room(models.Model):
    title = models.CharField(max_length=30, primary_key=True)
    description = models.CharField(max_length=200)
    members = models.ManyToManyField(User, related_name='room_members')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='room_creator')
    admins = models.ManyToManyField(User, blank=True, related_name='room_admins')
    onlineUsers = models.ManyToManyField(User, blank=True, related_name='room_online_users')
    requests = models.ManyToManyField(User, blank=True, related_name='room_requests')
    Lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE, related_name='room_lobby')

    def __str__(self):
        return self.title