from rest_framework.views import APIView

from apps.chat.serializers import MessageSerializer
from rest_framework.response import Response
from rest_framework import status
from apps.chat.main.models import Message

class GetNRecentMessages(APIView):
    def get(self, request, fromat=None):
        serializer = MessageSerializer(data=request.query_params)
        if serializer.is_valid():
            roomName = serializer.validated_data['roomName']
            time = serializer.validated_data['time']
            amount = serializer.validated_data['amount']
            messages = Message.objects.filter(room__title=roomName, date__gte=time).order_by('date')[:amount]
            mes = MessageSerializer(messages)
            return Response(data = mes, status=200)
