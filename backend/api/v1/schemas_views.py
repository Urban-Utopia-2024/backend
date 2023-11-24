from rest_framework import status, serializers
from drf_spectacular.utils import inline_serializer, extend_schema

from user.validators import (
    PASS_ERROR, USER_FIRST_NAME_ERROR, USER_LAST_NAME_ERROR,
)

from api.v1.serializers import (
    UserRegisterSerializer,
)


USER_SCHEMA = {
    'create': extend_schema(
        description='Создает нового пользователя.',
        summary='Создать нового пользователя.',
        responses={
            status.HTTP_201_CREATED: UserRegisterSerializer,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='users_create_error_400',
                fields={
                    'email': serializers.CharField(
                        default=(
                            'Пользователь с таким адресом электронной '
                            'почты уже зарегистрирован.'
                        ),
                    ),
                    'password': serializers.CharField(
                        default=PASS_ERROR,
                    ),
                    'first_name': serializers.CharField(
                        default=USER_FIRST_NAME_ERROR,
                    ),
                    'last_name': serializers.CharField(
                        default=USER_LAST_NAME_ERROR,
                    ),
                    'phone': serializers.CharField(
                        default=(
                            'Введенный номер телефона не действителен.'
                        ),
                    ),
                },
            ),
        },
    ),
}
