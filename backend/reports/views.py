from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from cases.models import Case
from .models import Report
from .serializers import ReportSerializer, CreateReportSerializer
from .evaluator import evaluate_report


@api_view(['POST'])
def submit_report(request):
    """
    Foydalanuvchi hisobotini qabul qiladi, AI orqali baholaydi,
    natijani saqlaydi va qaytaradi.
    """
    serializer = CreateReportSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data

    try:
        case = Case.objects.get(id=data['case_id'])
    except Case.DoesNotExist:
        return Response({"error": "Case topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    # AI orqali baholaymiz
    is_correct, feedback = evaluate_report(
        case, data['accused_character_name'], data['reasoning']
    )

    report = Report.objects.create(
        case=case,
        session_id=data['session_id'],
        accused_character_name=data['accused_character_name'],
        reasoning=data['reasoning'],
        is_correct=is_correct,
        ai_feedback=feedback,
    )

    return Response(ReportSerializer(report).data, status=status.HTTP_201_CREATED)