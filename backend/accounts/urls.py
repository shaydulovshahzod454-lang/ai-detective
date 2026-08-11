from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),   # tayyor, kutubxonadan
    path('me/', views.current_user, name='current-user'),
]