from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Case, Clue
from .serializers import CaseListSerializer, CaseDetailSerializer, ClueSerializer, CreateClueSerializer


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
    Bitta dalilni o'chiradi (foydalanuvchi xato qo'shgan bo'lsa).
    """
    try:
        clue = Clue.objects.get(id=clue_id)
    except Clue.DoesNotExist:
        return Response({"error": "Dalil topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    clue.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)