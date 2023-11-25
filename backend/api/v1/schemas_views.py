from rest_framework import status, serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer, TokenRefreshSerializer,
)
from drf_spectacular.utils import (
    OpenApiParameter,
    inline_serializer, extend_schema,
)

from user.validators import (
    PASS_ERROR, USER_FIRST_NAME_ERROR, USER_LAST_NAME_ERROR,
)
from api.v1.serializers import (
    AppealAdminSerializer, AppealAnswerSerializer, AppealRatingSerializer,
    AppealUserSerializer, AppealUserPostSerializer,
    NewsSerializer, NewsPostSerializer,
    UserFullSerializer, UserRegisterSerializer,
)

DEFAULT_400_REQUIRED: str = 'Обязательное поле.'
DEFAULT_401: str = 'Учетные данные не были предоставлены.'
DEFAULT_403: str = 'У вас недостаточно прав для выполнения данного действия.'
DEFAULT_404: str = 'Страница не найдена.'

APPEAL_SCHEMA = {
    'list': extend_schema(
        description='Возвращает список обращений.',
        summary='Получить список обращений.',
        responses={
            status.HTTP_200_OK: AppealAdminSerializer,
        },
    ),
    'retrieve': extend_schema(
        description='Возвращает обращение с указанным идентификатором.',
        summary='Получить обращение.',
        responses={
            status.HTTP_200_OK: AppealAdminSerializer,
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='appeals_retrieve_error_400',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401,
                    ),
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='appeals_retrieve_error_404',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_404
                    ),
                },
            ),
        },
    ),
    'create': extend_schema(
        description='Создает обращение.',
        summary='Создать обращение.',
        request=AppealUserPostSerializer,
        responses={
            status.HTTP_201_CREATED: AppealUserSerializer,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='appeals_create_error_400',
                fields={
                    'municipal_id': serializers.CharField(
                        default=DEFAULT_400_REQUIRED,
                    ),
                    'topic': serializers.CharField(
                        default=DEFAULT_400_REQUIRED,
                    ),
                    'text': serializers.CharField(
                        default=DEFAULT_400_REQUIRED,
                    ),
                    'address': serializers.CharField(
                        default=DEFAULT_400_REQUIRED,
                    ),
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='appeals_create_error_401',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401,
                    ),
                },
            ),
        },
    ),
    'post_answer': extend_schema(
        description=(
            'Оставляет ответ обращению с указанным идентификатором.'
        ),
        summary='Оставить ответ обращению.',
        request=AppealAnswerSerializer,
        responses={
            status.HTTP_200_OK: inline_serializer(
                name='appeals_post_answer_200',
                fields={
                    'rating': serializers.CharField(
                        default='Ответ обращению оставлен.',
                    ),
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='appeals_post_answer_error_400',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401,
                    ),
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='appeals_post_answer_error_403',
                fields={
                    'detail': serializers.CharField(
                        default=(
                            'Вы уже дали официальный ответ обращению.'
                        ),
                    ),
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='appeals_post_answer_error_404',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_404
                    ),
                },
            ),
        },
    ),
    'rate_answer': extend_schema(
        description=(
            'Оставляет оценку ответа обращения с указанным идентификатором.'
        ),
        summary='Оценить ответ обращения.',
        request=AppealRatingSerializer,
        responses={
            status.HTTP_200_OK: inline_serializer(
                name='appeals_rate_answer_200',
                fields={
                    'rating': serializers.CharField(
                        default='Благодарим за оценку ответа!',
                    ),
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='appeals_rate_answer_error_400',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401,
                    ),
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='appeals_rate_answer_error_403',
                fields={
                    'detail': serializers.CharField(
                        default=(
                            'Вы не можете поставить оценку '
                            'незавершенному обращению.'
                        ),
                    ),
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='appeals_rate_answer_error_404',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_404
                    ),
                },
            ),
        },
    ),
}

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
    'create': extend_schema(
        description='Создает новость.',
        summary='Создать новость.',
        request=NewsPostSerializer,
        responses={
            status.HTTP_201_CREATED: NewsSerializer,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='news_create_error_400',
                fields={
                    'category': serializers.CharField(
                        default=DEFAULT_400_REQUIRED,
                    ),
                    'text': serializers.CharField(
                        default=DEFAULT_400_REQUIRED,
                    ),
                    'address': serializers.CharField(
                        default=DEFAULT_400_REQUIRED,
                    ),
                    'quiz': serializers.CharField(
                        default={
                            'answers': {
                                'answers': (
                                    'В опросе не может быть менее 2 '
                                    'вариантов ответа.'
                                )
                            },
                        },
                    ),
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='news_post_error_401',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401,
                    ),
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='news_post_error_403',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_403,
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
        parameters=[
            OpenApiParameter(
                name='is_municipal',
                location=OpenApiParameter.QUERY,
                description='Статус муниципального учреждения.',
                required=False,
                type=bool,
            ),
        ],
        responses={
            status.HTTP_200_OK: UserFullSerializer,
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='users_list_error_400',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401,
                    ),
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='users_retrieve_error_403',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_403,
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
                name='users_retrieve_error_400',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401,
                    ),
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='users_retrieve_error_403',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_403,
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
