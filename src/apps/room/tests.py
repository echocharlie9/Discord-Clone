from rest_framework.test import APIRequestFactory
from apps.room.api.views import RoomViewSet
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

from rest_framework.test import APIClient

class RoomViewSetTest(APITestCase):

    def setUp(self):
        # create user
        self.user = User(username='a')
        self.user.save()
        self.user2 = User(username='b')
        self.user2.save()
        self.user3 = User(username='c')
        self.user3.save()
        self.user4 = User(username='d')
        self.user4.save()
        self.lobby = Lobby(title='Lobby1', description='test')
        self.lobby.save()
        self.room = Room(title='Room1', description='test', creator=self.user, Lobby=self.lobby)
        self.room.members.add(self.user)
        self.room.members.add(self.user2)
        self.room.requests.add(self.user3)
        self.room.save()

        self.room2 = Room(title='Room2', description='test2', creator=self.user, Lobby=self.lobby)
        self.room2.members.add(self.user)
        self.room2.members.add(self.user2)
        self.room2.members.add(self.user3)
        self.room2.admins.add(self.user2)
        self.room2.requests.add(self.user4)
        self.room2.save()

        self.room3 = Room(title='Room3', description='test3', creator=self.user, Lobby=self.lobby)
        self.room3.members.add(self.user)
        self.room3.members.add(self.user2)
        self.room3.members.add(self.user3)
        self.room3.admins.add(self.user2)
        self.room3.admins.add(self.user3)
        self.room3.save()
    def tearDown(self):
        pass

    def testDetailViewBasicFunctionality(self):
        # create request
        factory = APIRequestFactory()
        request = factory.get('/room/Room1', {}, format='json')
        force_authenticate(request, user=self.user)
        # create view
        view = RoomViewSet.as_view(actions={'get': 'retrieve'})
        # get response
        response = view(request, pk='Room1')
        room1 = response.data
        # print(room1)
        data = json.dumps(room1)
        # print(data)
        ser = RoomSerializer(data=data)
        if ser.is_valid():
            self.assertEqual(ser.validated_data, self.room)

    #creator kick user
    def testKickUser1(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        # print("room status before:" + str(Room.objects.get(title='Room1').members.all()))
        response = client.post('/room/Room1/KickUser/', {'username': 'b'})
        # print('response:' + str(response))
        # check user2 is not in Room.objects.get(title='Room1').members
        assert(str(Room.objects.get(title='Room1').members.all()) == '<QuerySet [<User: a>]>')
        # print("test kick user:" + str(Room.objects.get(title='Room1').members.all()))
    
    #creator kicking a nonexisting user
    def testKickUser2(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        # print("room status before:" + str(Room.objects.get(title='Room1').members.all()))
        response = client.post('/room/Room1/KickUser/', {'username': 'c'})
        # print('response:' + str(response))
        # check user2 is not in Room.objects.get(title='Room1').members
        assert(str(Room.objects.get(title='Room1').members.all()) ==  '<QuerySet [<User: a>, <User: b>]>')

    #non admin attempting to kick a user
    def testKickUser2(self):
        client = APIClient()
        client.force_authenticate(user=self.user2)
        # print("room status before:" + str(Room.objects.get(title='Room1').members.all()))
        response = client.post('/room/Room1/KickUser/', {'username': 'a'})
        # print('response:' + str(response))
        assert(str(Room.objects.get(title='Room1').members.all()) ==  '<QuerySet [<User: a>, <User: b>]>')
    
    #admin kick a user
    def testKickUser3(self):
        client = APIClient()
        client.force_authenticate(user=self.user2)
        # print("room status before:" + str(Room.objects.get(title='Room1').members.all()))
        response = client.post('/room/Room2/KickUser/', {'username': 'c'})
        # print('response:' + str(response))
        assert(str(Room.objects.get(title='Room2').members.all()) ==  '<QuerySet [<User: a>, <User: b>]>')

    #admin kick creator
    def testKickUser4(self):
        client = APIClient()
        client.force_authenticate(user=self.user2)
        # print("room status before:" + str(Room.objects.get(title='Room1').members.all()))
        response = client.post('/room/Room2/KickUser/', {'username': 'a'})
        # print('response:' + str(response))
        assert(str(Room.objects.get(title='Room2').members.all()) ==  '<QuerySet [<User: a>, <User: b>, <User: c>]>')

    #creator accepting user
    def testAcceptUser1(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        # print(str(Room.objects.get(title='Room1').members.all()))
        response = client.post('/room/Room1/AcceptUser/', {'username': 'c'})
        # print(response)
        assert(str(Room.objects.get(title='Room1').members.all()) == '<QuerySet [<User: a>, <User: b>, <User: c>]>')

    #creator accepts a user that is not requesting to join
    def testAcceptUser2(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        # print(str(Room.objects.get(title='Room1').members.all()))
        response = client.post('/room/Room1/AcceptUser/', {'username': 'a'})
        # print(response)
        assert(str(Room.objects.get(title='Room1').members.all()) == '<QuerySet [<User: a>, <User: b>]>')

    #admin accepting user 
    def testAcceptUser3(self):
        client = APIClient()
        client.force_authenticate(user=self.user2)
        # print(str(Room.objects.get(title='Room1').members.all()))
        response = client.post('/room/Room2/AcceptUser/', {'username': 'd'})
        # print(response)
        assert(str(Room.objects.get(title='Room2').members.all()) == '<QuerySet [<User: a>, <User: b>, <User: c>, <User: d>]>')

    #nonadmin accepting user 
    def testAcceptUser4(self):
        client = APIClient()
        client.force_authenticate(user=self.user3)
        # print(str(Room.objects.get(title='Room1').members.all()))
        response = client.post('/room/Room2/AcceptUser/', {'username': 'd'})
        # print(response)
        assert(str(Room.objects.get(title='Room2').members.all()) == '<QuerySet [<User: a>, <User: b>, <User: c>]>')

    #creator promotes member to admin
    def testPromoteUser1(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post('/room/Room2/PromoteUser/', {'username': 'c'})
        assert(str(Room.objects.get(title='Room2').admins.all()) == '<QuerySet [<User: b>, <User: c>]>')

    #admin promotes member to admin
    def testPromoteUser2(self):
        client = APIClient()
        client.force_authenticate(user=self.user2)
        response = client.post('/room/Room2/PromoteUser/', {'username': 'c'})
        assert(str(Room.objects.get(title='Room2').admins.all()) == '<QuerySet [<User: b>, <User: c>]>')

    #member attempts to promote
    def testPromoteUser3(self):
        client = APIClient()
        client.force_authenticate(user=self.user3)
        response = client.post('/room/Room2/PromoteUser/', {'username': 'c'})
        assert(str(Room.objects.get(title='Room2').admins.all()) == '<QuerySet [<User: b>]>')

    #creator attempts to promote admin
    def testPromoteUser4(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post('/room/Room2/PromoteUser/', {'username': 'b'})
        assert(str(Room.objects.get(title='Room2').admins.all()) == '<QuerySet [<User: b>]>')

    #admin attempts to promote admin
    def testPromoteUser5(self):
        client = APIClient()
        client.force_authenticate(user=self.user2)
        response = client.post('/room/Room2/PromoteUser/', {'username': 'b'})
        assert(str(Room.objects.get(title='Room2').admins.all()) == '<QuerySet [<User: b>]>')

    #creator demotes admin
    def testDemoteUser1(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post('/room/Room2/DemoteUser/', {'username': 'b'})
        assert(str(Room.objects.get(title='Room2').admins.all()) == '<QuerySet []>')

    #admin attempts to demote creator
    def testDemoteUser2(self):
        client = APIClient()
        client.force_authenticate(user=self.user2)
        response = client.post('/room/Room2/DemoteUser/', {'username': 'a'})
        assert(str(Room.objects.get(title='Room2').admins.all()) == '<QuerySet [<User: b>]>')
    
    # admin attempts to demote admin
    def testDemoteUser3(self):
        client = APIClient()
        client.force_authenticate(user=self.user2)
        response = client.post('/room/Room3/DemoteUser/', {'username': 'c'})
        assert(str(Room.objects.get(title='Room3').admins.all()) == '<QuerySet [<User: b>, <User: c>]>')

    #member attempts to demote
    def testDemoteUser4(self):
        client = APIClient()
        client.force_authenticate(user=self.user3)
        response = client.post('/room/Room3/DemoteUser/', {'username': 'c'})
        assert(str(Room.objects.get(title='Room2').admins.all()) == '<QuerySet [<User: b>]>')