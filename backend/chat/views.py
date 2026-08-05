from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from cases.models import Character
from .models import ChatMessage
from .serializers import ChatMessageSerializer, SendMessageSerializer
from .ai_service import ask_character


@api_view(['POST'])
def send_message(request):
    """
    Foydalanuvchidan xabar qabul qiladi, AI'ga yuboradi,
    javobni qaytaradi va ikkalasini ham ma'lumotlar bazasiga saqlaydi.
    """
    # 1. Kelgan ma'lumotni tekshiramiz
    serializer = SendMessageSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    character_id = serializer.validated_data['character_id']
    user_message = serializer.validated_data['message']
    session_id = serializer.validated_data['session_id']

    # 2. Personajni topamiz
    try:
        character = Character.objects.get(id=character_id)
    except Character.DoesNotExist:
        return Response({"error": "Personaj topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    # 3. Shu sessiyaning oldingi xabarlarini olamiz (suhbat tarixi uchun)
    previous_messages = ChatMessage.objects.filter(
        character=character, session_id=session_id
    ).order_by('created_at')

    conversation_history = [
        {"role": msg.role, "content": msg.content} for msg in previous_messages
    ]

    # 4. Foydalanuvchi xabarini saqlaymiz
    ChatMessage.objects.create(
        character=character, role='user', content=user_message, session_id=session_id
    )

    # 5. AI'dan javob olamiz
    ai_response = ask_character(character, user_message, conversation_history)

    # 6. AI javobini ham saqlaymiz
    ChatMessage.objects.create(
        character=character, role='assistant', content=ai_response, session_id=session_id
    )

    # 7. Frontend'ga javob qaytaramiz
    return Response({"response": ai_response})


@api_view(['GET'])
def get_chat_history(request, character_id, session_id):
    """
    Shu personaj va sessiya uchun butun suhbat tarixini qaytaradi.
    Sahifa yangilanganda frontend shu orqali suhbatni tiklaydi.
    """
    messages = ChatMessage.objects.filter(character_id=character_id, session_id=session_id)
    serializer = ChatMessageSerializer(messages, many=True)
    return Response(serializer.data)