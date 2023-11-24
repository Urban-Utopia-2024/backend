from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from user.models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Переопределяет TokenObtainPairSerializer для access токена:
        - добавляет поле is_staff, если оно True
        - добавляет поле is_municipal, если оно True
    """
    @classmethod
    def get_token(cls, user):
        token: dict[str, any] = super().get_token(user)
        for attr in ('is_staff', 'is_municipal'):
            val: bool = getattr(user, attr)
            if val:
                token[attr] = user.is_staff
        return token


class UserRegisterSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя."""

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'first_name',
            'last_name',
            'phone',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        isinstance: User = super().create(validated_data)
        isinstance.set_password(isinstance.password)
        isinstance.save()
        return isinstance
