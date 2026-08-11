from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])   # ro'yxatdan o'tish uchun login shart emas
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.save()

    # Ro'yxatdan o'tgach, darhol token ham beramiz — foydalanuvchi
    # alohida login qilmasdan tizimga kiradi
    refresh = RefreshToken.for_user(user)

    return Response({
        'user': UserSerializer(user).data,
        'access': str(refresh.access_token),
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])   # faqat login qilganlar ko'ra oladi
def current_user(request):
    """
    Frontend sahifa yuklanganda "men kimman" deb so'rash uchun.
    """
    return Response(UserSerializer(request.user).data)