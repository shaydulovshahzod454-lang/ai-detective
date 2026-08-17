from rest_framework import serializers
from .models import Case, Scene, Character, Clue, CaseCollaborator
from django.contrib.auth.models import User


class CharacterListSerializer(serializers.ModelSerializer):
    """
    Personajlar ro'yxati uchun — QISQA ma'lumot.
    """
    image = serializers.SerializerMethodField()  # ← o'zgardi

    class Meta:
        model = Character
        fields = ['id', 'name', 'image', 'scene']

    def get_image(self, obj):
        """
        Rasmning TO'LIQ manzilini qaytaradi (domen bilan birga),
        shunchaki nisbiy yo'l emas.
        """
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class SceneSerializer(serializers.ModelSerializer):
    characters = CharacterListSerializer(many=True, read_only=True)

    class Meta:
        model = Scene
        fields = ['id', 'name', 'description', 'background_image', 'characters']


class CaseListSerializer(serializers.ModelSerializer):
    """
    Case'lar ro'yxati uchun — juda qisqa, faqat asosiy ma'lumot.
    """
    class Meta:
        model = Case
        fields = ['id', 'title', 'description']


class CaseDetailSerializer(serializers.ModelSerializer):
    """
    Bitta case ichiga kirilganda — to'liq ma'lumot: barcha scene va character'lar bilan.
    DIQQAT: 'solution' maydoni bu yerda ham YO'Q.
    """
    scenes = SceneSerializer(many=True, read_only=True)
    unassigned_characters = serializers.SerializerMethodField()

    class Meta:
        model = Case
        fields = ['id', 'title', 'description', 'scenes', 'unassigned_characters']

    def get_unassigned_characters(self, obj):
        """
        Hech qanday scene'ga biriktirilmagan personajlar — bular ham
        o'yinchiga ko'rinishi va suhbatlashish uchun ochiq bo'lishi kerak.
        """
        characters = obj.characters.filter(scene__isnull=True)
        return CharacterListSerializer(characters, many=True, context=self.context).data

class ClueSerializer(serializers.ModelSerializer):
    source_character_name = serializers.CharField(source='source_character.name', read_only=True)

    class Meta:
        model = Clue
        fields = ['id', 'text', 'source_character', 'source_character_name', 'created_at']


class CreateClueSerializer(serializers.Serializer):
    """
    Yangi dalil yaratish uchun kiruvchi ma'lumotni tekshiradi.
    """
    case_id = serializers.IntegerField()
    session_id = serializers.CharField(max_length=100)
    text = serializers.CharField(max_length=500)
    source_character_id = serializers.IntegerField(required=False, allow_null=True)

class CaseCollaboratorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = CaseCollaborator
        fields = ['id', 'username', 'added_at']


class MyCaseSerializer(serializers.ModelSerializer):
    """
    'Mening case'larim' ro'yxati uchun — muallif ekanligini ham ko'rsatadi.
    """
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Case
        fields = ['id', 'title', 'description', 'is_active', 'is_owner']

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return obj.created_by_id == request.user.id


class CreateCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['title', 'description', 'solution']

class CaseEditSerializer(serializers.ModelSerializer):
    """
    Tahrirlash sahifasi uchun — 'solution' HAM ko'rinadi, chunki bu
    yerga faqat egasi/hamkor kiradi (case_detail'dagi ommaviy
    serializer'dan farqli, u yerda solution atayin yashirilgan edi).
    """
    class Meta:
        model = Case
        fields = ['id', 'title', 'description', 'solution', 'is_active']


class UpdateCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['title', 'description', 'solution']

class SceneEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scene
        fields = ['id', 'name', 'description', 'background_image']


class CharacterEditSerializer(serializers.ModelSerializer):
    """
    Tahrirlash uchun — BARCHA maydonlar ko'rinadi (knowledge, secrets ham),
    chunki bu yerga faqat egasi/hamkor kiradi.
    """
    class Meta:
        model = Character
        fields = [
            'id', 'name', 'image', 'scene',
            'personality', 'knowledge', 'secrets',
            'alibi', 'relationships', 'is_guilty', 'lying_tendency',
        ]