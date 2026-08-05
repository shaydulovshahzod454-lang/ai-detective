from rest_framework import serializers
from .models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    """
    ChatMessage modelini JSON'ga aylantiradi (frontend uchun).
    """
    class Meta:
        model = ChatMessage
        fields = ['id', 'role', 'content', 'created_at']


class SendMessageSerializer(serializers.Serializer):
    """
    Frontend'dan keladigan so'rovni tekshiradi (validatsiya qiladi).
    Bu model emas — shunchaki kiruvchi ma'lumotning 'shakli' qanday bo'lishi kerakligini belgilaydi.
    """
    character_id = serializers.IntegerField()
    message = serializers.CharField(max_length=1000)
    session_id = serializers.CharField(max_length=100)