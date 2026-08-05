from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'accused_character_name', 'reasoning', 'is_correct', 'ai_feedback', 'created_at']


class CreateReportSerializer(serializers.Serializer):
    case_id = serializers.IntegerField()
    session_id = serializers.CharField(max_length=100)
    accused_character_name = serializers.CharField(max_length=100)
    reasoning = serializers.CharField(max_length=2000)