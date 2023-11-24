from rest_framework import status, serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer, TokenRefreshSerializer,
)
from drf_spectacular.utils import inline_serializer, extend_schema

from user.validators import (
    PASS_ERROR, USER_FIRST_NAME_ERROR, USER_LAST_NAME_ERROR,
)
from api.v1.serializers import (
    NewsSerializer, UserFullSerializer, UserRegisterSerializer,
)

DEFAULT_401: str = 'Учетные данные не были предоставлены.'
DEFAULT_404: str = 'Страница не найдена.'

NEWS_SCHEMA = {
    'list': extend_schema(
        description='Возвращает список новостей.',
        summary='Получить список новостей.',
        responses={
            status.HTTP_200_OK: NewsSerializer,
        },
    ),
    'retrieve': extend_schema(
        description='Возвращает новость с указанным идентификатором.',
        summary='Получить новость.',
        responses={
            status.HTTP_200_OK: NewsSerializer,
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='news_retrieve_error_404',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_404
                    ),
                },
            ),
        },
    ),
}

TOKEN_OBTAIN_SCHEMA: dict[str, str] = {
    'description': (
        'Принимает набор учетных данных пользователя и возвращает '
        'пару JWT-токенов доступа и обновления.'
    ),
    'summary': 'Получить пару JWT-токенов доступа и обновления.',
    'responses': {
        status.HTTP_200_OK: TokenObtainPairSerializer,
        status.HTTP_400_BAD_REQUEST: inline_serializer(
            name='token_pair_create_error_400',
            fields={
                'detail': serializers.CharField(
                    default=(
                        'No active account found with the given credentials'
                    ),
                ),
            },
        ),
    },
}

TOKEN_REFRESH_SCHEMA: dict[str, str] = {
    'description': (
        'Принимает JWT-токен обновления и возвращает JWT-токен доступа, '
        'если токен обновления действителен.'
    ),
    'summary': 'Обновить JWT-токен доступа.',
    'responses': {
        status.HTTP_200_OK: TokenRefreshSerializer,
        status.HTTP_400_BAD_REQUEST: inline_serializer(
            name='access_token_refresh_error_400',
            fields={
                'detail': serializers.CharField(
                    default='Token is invalid or expired',
                ),
                'code': serializers.CharField(
                    default='token_not_valid',
                ),
            },
        ),
    },
}

USERS_SCHEMA = {
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
    'list': extend_schema(
        description='Возвращает список пользователей.',
        summary='Получить список пользователей.',
        responses={
            status.HTTP_200_OK: UserFullSerializer,
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='users_create_error_400',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401,
                    ),
                },
            ),
        },
    ),
    'retrieve': extend_schema(
        description='Возвращает пользователя с указанным идентификатором.',
        summary='Получить пользователей.',
        responses={
            status.HTTP_200_OK: UserFullSerializer,
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='users_create_error_400',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401,
                    ),
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='user_retrieve_error_404',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_404
                    ),
                },
            ),
        },
    ),
}
