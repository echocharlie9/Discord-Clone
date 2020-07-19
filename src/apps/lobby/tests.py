from rest_framework.test import APIRequestFactory
from apps.lobby.api.views import LobbyViewSet
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model as user_model
User = user_model()
from apps.lobby.main.models import Lobby
from apps.room.main.models import Room
from rest_framework.test import force_authenticate
from apps.room.main.serializers import RoomSerializer
import io
from rest_framework.parsers import JSONParser
import json


class LobbyViewSetTest(APITestCase):

    def setUp(self):
        # create user
        self.user = User(username='a')
        self.user.save()
        self.lobby = Lobby(title='Lobby1', description='test')
        self.lobby.save()
        self.room = Room(title='Room1', description='test', creator=self.user, Lobby=self.lobby)
        self.room.members.add(self.user)
        self.room.save()


    def tearDown(self):
        pass

    def testDetailViewBasicFunctionality(self):
        # create request
        factory = APIRequestFactory()
        request = factory.get('/lobby/Lobby1', {}, format='json')
        force_authenticate(request, user=self.user)
        # create view
        view = LobbyViewSet.as_view(actions={'get': 'retrieve'})
        # get response
        response = view(request, pk='Lobby1')
        room1 = response.data['room_lobby'][0]
        print(room1)
        data = json.dumps(room1)
        print(data)
        ser = RoomSerializer(data=data)
        if ser.is_valid():
            self.assertEqual(ser.validated_data, self.room)