from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send_message, name='send-message'),
    path('history/<int:character_id>/<str:session_id>/', views.get_chat_history, name='chat-history'),
]