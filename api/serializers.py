from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.Serializer):
    username     = serializers.CharField()
    password     = serializers.CharField(write_only=True)
    company_name = serializers.CharField()
    email        = serializers.EmailField()

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class KBQuerySerializer(serializers.Serializer):
    search = serializers.CharField()

    def validate_search(self, value):
        if not value.strip():
            raise serializers.ValidationError("Search field cannot be blank.")
        return value