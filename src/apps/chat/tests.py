from rest_framework.test import APIRequestFactory
from apps.room.api.views import RoomViewSet
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model as user_model
User = user_model()
from django.conf.urls import url
from channels.routing import URLRouter
from apps.lobby.main.models import Lobby
from apps.room.main.models import Room
from rest_framework.test import force_authenticate
from apps.room.main.serializers import RoomSerializer
import io
from rest_framework.parsers import JSONParser
import json
from rest_framework.test import APIClient
import pytest
from apps.chat.api.consumers import ChatConsumer
from channels.testing import WebsocketCommunicator
import asyncio
from asgiref.sync import sync_to_async

application = URLRouter([
    url(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer),
])

@pytest.mark.django_db
class Test:
    def setup(self):
        user = User(username='a')
        user.save()
        lobby = Lobby(title='Lobby1', description='test')
        lobby.save()
        room = Room(title='Room1', description='test', creator=user, Lobby=lobby)
        room.members.add(user)
        room.save()
    # @sync_to_async
    # def makeUser():
    #     user = User(username='a')
    #     user.save()
    #     return user

    # @sync_to_async
    # def makeLobby():
    #     lobby = Lobby(title='Lobby1', description='test')
    #     lobby.save()
    #     return lobby

    # @sync_to_async
    # def makeRoom(user, lobby):
    #     room = Room(title='Room1', description='test', creator=user, Lobby=lobby)
    #     room.members.add(user)
    #     room.save()

    @pytest.mark.asyncio
    async def test_BasicFunctionality(self):
        # user = await makeUser()
        # lobby = await makeLobby()
        # await makeRoom(user, lobby)
        # assert False
        communicator = WebsocketCommunicator(application, "/ws/chat/Room1/")
        connected, subprotocol = await communicator.connect()
        assert connected
        # Test sending text
        await communicator.send_json_to({"message": "hello"})
        response = await communicator.receive_from()
        print('asdfasdfd' + response)
        print(type(response))
        print(type(json.loads(response)))
        assert json.loads(response)['message'] == "hello"
        # Close
        await communicator.disconnect()
