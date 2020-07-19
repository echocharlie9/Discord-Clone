from rest_framework import serializers

from apps.room.main.serializers import RoomSerializer

from .models import Lobby

class LobbySerializer(serializers.ModelSerializer):
    room_lobby = RoomSerializer(many=True, read_only=True)
    class Meta:
        model = Lobby
        fields = ['title','room_lobby']
        