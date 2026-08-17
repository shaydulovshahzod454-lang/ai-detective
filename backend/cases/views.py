from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import Case, Clue, CaseCollaborator, Scene, Character
from .serializers import (
    CaseListSerializer, CaseDetailSerializer, ClueSerializer, 
    CreateClueSerializer, CaseCollaboratorSerializer, MyCaseSerializer, CreateCaseSerializer,
    CaseEditSerializer, UpdateCaseSerializer, SceneEditSerializer, CharacterEditSerializer
)
from .permissions import IsCaseOwnerOrCollaborator

@api_view(['GET'])
def case_list(request):
    """
    Faol (is_active=True) barcha case'lar ro'yxatini qaytaradi.
    """
    cases = Case.objects.filter(is_active=True)
    serializer = CaseListSerializer(cases, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def case_detail(request, case_id):
    try:
        case = Case.objects.get(id=case_id, is_active=True)
    except Case.DoesNotExist:
        return Response({"error": "Case topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CaseDetailSerializer(case, context={'request': request})  # ← context qo'shildi
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def clue_list_create(request):
    """
    GET — shu case va sessiya uchun barcha dalillarni qaytaradi.
    POST — yangi dalil qo'shadi.
    """
    if request.method == 'GET':
        case_id = request.query_params.get('case_id')
        session_id = request.query_params.get('session_id')

        if not case_id or not session_id:
            return Response(
                {"error": "case_id va session_id kerak"},
                status=status.HTTP_400_BAD_REQUEST
            )

        clues = Clue.objects.filter(case_id=case_id, session_id=session_id)
        serializer = ClueSerializer(clues, many=True)
        return Response(serializer.data)

    # POST
    serializer = CreateClueSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    clue = Clue.objects.create(
        case_id=serializer.validated_data['case_id'],
        session_id=serializer.validated_data['session_id'],
        text=serializer.validated_data['text'],
        source_character_id=serializer.validated_data.get('source_character_id'),
    )

    return Response(ClueSerializer(clue).data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def clue_delete(request, clue_id):
    """
    Bitta dalilni o'chiradi. session_id URL query orqali talab qilinadi,
    faqat shu sessiyaga tegishli dalil o'chirilishi mumkin.
    """
    session_id = request.query_params.get('session_id')
    if not session_id:
        return Response({"error": "session_id kerak"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        clue = Clue.objects.get(id=clue_id, session_id=session_id)
    except Clue.DoesNotExist:
        return Response({"error": "Dalil topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    clue.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def my_cases(request):
    """
    GET — foydalanuvchi EGASI bo'lgan yoki HAMKOR bo'lgan barcha case'larni qaytaradi.
    POST — yangi case yaratadi, avtomatik shu foydalanuvchini muallif qiladi.
    """
    if request.method == 'GET':
        cases = Case.objects.filter(
            Q(created_by=request.user) | Q(collaborators__user=request.user)
        ).distinct()
        serializer = MyCaseSerializer(cases, many=True, context={'request': request})
        return Response(serializer.data)

    # POST
    serializer = CreateCaseSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    case = serializer.save(created_by=request.user, is_active=False)  # draft holatda boshlanadi
    return Response(MyCaseSerializer(case, context={'request': request}).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def case_collaborators(request, case_id):
    """
    GET — shu case'ning hamkorlar ro'yxati.
    POST — yangi hamkor qo'shadi (faqat case EGASI qo'sha oladi).
    """
    try:
        case = Case.objects.get(id=case_id)
    except Case.DoesNotExist:
        return Response({"error": "Case topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Ko'rish uchun — egasi yoki hamkor bo'lish kifoya
        if case.created_by_id != request.user.id and not case.collaborators.filter(user=request.user).exists():
            return Response({"error": "Ruxsat yo'q"}, status=status.HTTP_403_FORBIDDEN)
        serializer = CaseCollaboratorSerializer(case.collaborators.all(), many=True)
        return Response(serializer.data)

    # POST — qo'shish uchun FAQAT egasi ruxsat etiladi
    if case.created_by_id != request.user.id:
        return Response(
            {"error": "Faqat case egasi hamkor qo'sha oladi"},
            status=status.HTTP_403_FORBIDDEN
        )

    username = request.data.get('username')
    if not username:
        return Response({"error": "username kerak"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_to_add = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"error": "Bunday foydalanuvchi topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    if user_to_add.id == case.created_by_id:
        return Response({"error": "Bu foydalanuvchi allaqachon case egasi"}, status=status.HTTP_400_BAD_REQUEST)

    collaborator, created = CaseCollaborator.objects.get_or_create(case=case, user=user_to_add)
    if not created:
        return Response({"error": "Bu foydalanuvchi allaqachon hamkor"}, status=status.HTTP_400_BAD_REQUEST)

    return Response(CaseCollaboratorSerializer(collaborator).data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_collaborator(request, case_id, collaborator_id):
    """
    Hamkorni case'dan olib tashlaydi (faqat case egasi qila oladi).
    """
    try:
        case = Case.objects.get(id=case_id)
    except Case.DoesNotExist:
        return Response({"error": "Case topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    if case.created_by_id != request.user.id:
        return Response({"error": "Ruxsat yo'q"}, status=status.HTTP_403_FORBIDDEN)

    try:
        collaborator = case.collaborators.get(id=collaborator_id)
    except CaseCollaborator.DoesNotExist:
        return Response({"error": "Hamkor topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    collaborator.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

def _check_edit_permission(case, user):
    """
    Yordamchi funksiya: foydalanuvchi shu case'ni tahrirlay oladimi, tekshiradi.
    Bir nechta view'da takrorlanmasligi uchun alohida chiqardik.
    """
    if case.created_by_id == user.id:
        return True
    return case.collaborators.filter(user=user).exists()


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def case_edit(request, case_id):
    """
    GET — tahrirlash uchun to'liq ma'lumot (solution bilan birga).
    PATCH — sarlavha/tavsif/yechimni yangilaydi.
    Ikkalasi ham faqat egasi yoki hamkor uchun ruxsat etiladi.
    """
    try:
        case = Case.objects.get(id=case_id)
    except Case.DoesNotExist:
        return Response({"error": "Case topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    if not _check_edit_permission(case, request.user):
        return Response({"error": "Ruxsat yo'q"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        return Response(CaseEditSerializer(case).data)

    # PATCH
    serializer = UpdateCaseSerializer(case, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    return Response(CaseEditSerializer(case).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def case_publish(request, case_id):
    """
    Case'ning is_active holatini almashtiradi (qoralama ↔ faol).
    Faqat EGASI qila oladi — hamkorlar nashr qilish huquqiga ega emas,
    bu qaror faqat asosiy muallifga tegishli.
    """
    try:
        case = Case.objects.get(id=case_id)
    except Case.DoesNotExist:
        return Response({"error": "Case topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    if case.created_by_id != request.user.id:
        return Response({"error": "Faqat case egasi nashr qila oladi"}, status=status.HTTP_403_FORBIDDEN)

    case.is_active = not case.is_active
    case.save()
    return Response(CaseEditSerializer(case).data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])   # rasm yuklash uchun kerak
def scene_list_create(request, case_id):
    try:
        case = Case.objects.get(id=case_id)
    except Case.DoesNotExist:
        return Response({"error": "Case topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    if not _check_edit_permission(case, request.user):
        return Response({"error": "Ruxsat yo'q"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        scenes = case.scenes.all()
        serializer = SceneEditSerializer(scenes, many=True, context={'request': request})
        return Response(serializer.data)

    # POST
    serializer = SceneEditSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    scene = serializer.save(case=case)
    return Response(SceneEditSerializer(scene, context={'request': request}).data, status=status.HTTP_201_CREATED)


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def scene_detail_edit(request, case_id, scene_id):
    try:
        case = Case.objects.get(id=case_id)
        scene = case.scenes.get(id=scene_id)
    except (Case.DoesNotExist, Scene.DoesNotExist):
        return Response({"error": "Topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    if not _check_edit_permission(case, request.user):
        return Response({"error": "Ruxsat yo'q"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'DELETE':
        scene.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # PATCH
    serializer = SceneEditSerializer(scene, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response(SceneEditSerializer(scene, context={'request': request}).data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def character_list_create(request, case_id):
    try:
        case = Case.objects.get(id=case_id)
    except Case.DoesNotExist:
        return Response({"error": "Case topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    if not _check_edit_permission(case, request.user):
        return Response({"error": "Ruxsat yo'q"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        characters = case.characters.all()
        serializer = CharacterEditSerializer(characters, many=True, context={'request': request})
        return Response(serializer.data)

    # POST
    serializer = CharacterEditSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    character = serializer.save(case=case)
    return Response(CharacterEditSerializer(character, context={'request': request}).data, status=status.HTTP_201_CREATED)


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def character_detail_edit(request, case_id, character_id):
    try:
        case = Case.objects.get(id=case_id)
        character = case.characters.get(id=character_id)
    except (Case.DoesNotExist, Character.DoesNotExist):
        return Response({"error": "Topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    if not _check_edit_permission(case, request.user):
        return Response({"error": "Ruxsat yo'q"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'DELETE':
        character.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # PATCH
    serializer = CharacterEditSerializer(character, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response(CharacterEditSerializer(character, context={'request': request}).data)