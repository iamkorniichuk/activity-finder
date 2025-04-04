from django.contrib.auth.password_validation import (
    validate_password as django_validate_password,
)
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "refresh", "access")
        extra_kwargs = {
            "password": {"write_only": True},
            "username": {"write_only": True},
        }

    refresh = serializers.SerializerMethodField()
    access = serializers.SerializerMethodField()

    def get_refresh(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token)

    def get_access(self, obj):
        token = RefreshToken.for_user(obj).access_token
        return str(token)

    def validate_password(self, password):
        current_user = self.instance
        django_validate_password(password, current_user)
        return password
