from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

# importing serializers
from apps.room.main.serializers import RoomSerializer
from apps.myauth.main.serializers import UserSerializer, GetUserSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

# importing models
from apps.room.main.models import Room

from apps.room.main.permissions import RoomCreator, RoomMember, RoomAdmin, KickPermission

from rest_framework.response import Response

from django.shortcuts import get_object_or_404
# lobbies can only be read 
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @action(detail=True, methods=['post'], permission_classes=(RoomCreator, RoomAdmin))
    def KickUser(self, request, pk):
        room = self.get_object()
        serializer = GetUserSerializer(data=dict(request.data.dict()))
        if serializer.is_valid():
            user = get_object_or_404(User, username = serializer.validated_data['username'])
            #edge case where admin cannot kick creator
            if user in room.members.all() and user != room.creator:
                room.members.remove(user)
                return Response(data=request.data, status= 200)
            return Response(data=request.data, status= 400)
        return Response(data=request.data, status= 400)

    @action(detail=True, methods=['post'], permission_classes=(RoomCreator, RoomAdmin))
    def AcceptUser(self, request, pk):
        room = self.get_object()
        serializer = GetUserSerializer(data=dict(request.data.dict()))
        if serializer.is_valid():
            user = get_object_or_404(User, username = serializer.validated_data['username'])
            if user in room.requests.all():
                room.members.add(user)
                return Response(data=request.data, status= 200)
            return Response(data=request.data, status= 400)
        return Response(data=request.data, status= 400)

    @action(detail=True, methods=['post'], permission_classes=(RoomCreator, RoomAdmin))
    def PromoteUser(self, request, pk):
        room = self.get_object()
        serializer = GetUserSerializer(data=dict(request.data.dict()))
        if serializer.is_valid():
            user = get_object_or_404(User, username = serializer.validated_data['username'])
            if user in room.members.all() and user not in room.admins.all():
                room.admins.add(user)
                return Response(data=request.data, status= 200)
            return Response(data=request.data, status= 400)
        return Response(data=request.data, status= 400)

    @action(detail=True, methods=['post'], permission_classes=(RoomCreator, RoomAdmin))
    def DemoteUser(self, request, pk):
        room = self.get_object()
        print("user " + str(request.user))
        serializer = GetUserSerializer(data=dict(request.data.dict()))
        if serializer.is_valid():
            user = get_object_or_404(User, username = serializer.validated_data['username'])
            if user in room.members.all() and user in room.admins.all() and user != room.creator and not (request.user in room.admins.all() and user in room.admins.all()):
                room.admins.remove(user)
                return Response(data=request.data, status= 200)
            return Response(data=request.data, status= 400)
        return Response(data=request.data, status= 400)

    def get_permissions(self):
        if self.action in ['create', 'list']:
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [RoomMember]
        else:
            # permission_classes = [RoomCreator]
            permission_classes = [KickPermission]
        return [permission() for permission in permission_classes]