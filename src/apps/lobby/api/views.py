from rest_framework import viewsets

# importing serializers
from apps.lobby.main.serializers import LobbySerializer

# importing models
from apps.lobby.main.models import Lobby

from rest_framework.permissions import IsAuthenticated, IsAdminUser

# lobbies can only be read 
class LobbyViewSet(viewsets.ModelViewSet):
    queryset = Lobby.objects.all()
    serializer_class = LobbySerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]




