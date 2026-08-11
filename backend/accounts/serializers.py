from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        # create_user — parolni avtomatik "hash" qilib saqlaydi (xavfsizlik uchun,
        # hech qachon oddiy matn ko'rinishida saqlanmaydi)
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']