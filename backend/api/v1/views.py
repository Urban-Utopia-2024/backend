from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,
)

from api.v1.permissions import IsMunicipal
from api.v1.serializers import (
    AppealAdminSerializer, AppealAnswerSerializer, AppealMunicipalSerializer,
    AppealRatingSerializer, AppealUserSerializer, AppealUserPostSerializer,
    NewsSerializer, NewsCommentSerializer, NewsPostSerializer,
    UserFullSerializer, UserRegisterSerializer,
)
from api.v1.schemas_views import (
    APPEAL_SCHEMA, DEFAULT_400_REQUIRED, NEWS_SCHEMA, TOKEN_OBTAIN_SCHEMA,
    TOKEN_REFRESH_SCHEMA, USERS_SCHEMA,
)
from info.models import Appeal, News, NewsComment
from urban_utopia_2024.app_data import APPEAL_STAGE_COMPLETED
from user.models import User


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        email: str = request.data.get('email')
        password: str = request.data.get('password')
        if email is None or password is None:
            return Response(
                data={
                    'email': DEFAULT_400_REQUIRED,
                    'password': DEFAULT_400_REQUIRED,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        user: User = authenticate(email=email, password=password)
        if not User:
            return Response(
                data={
                    'detail': 'Указаны неверные email или password.'
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        token, _ = Token.objects.get_or_create(user=user)
        response_data: dict[str, str] = {
            'token': token.key,
            'user_id': user.pk,
        }
        for attr in ('is_municipal', 'is_staff'):
            if getattr(user, attr):
                response_data[attr]: bool = True
        return Response(
            data=response_data,
            status=status.HTTP_200_OK,
        )


@extend_schema_view(**APPEAL_SCHEMA)
class AppealViewSet(ModelViewSet):
    """ViewSet для взаимодействия с моделью обращений."""

    http_method_names = ('get', 'post',)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AppealAdminSerializer
        if self.request.user.is_municipal:
            return AppealMunicipalSerializer
        if self.request.method == 'POST':
            return AppealUserPostSerializer
        return AppealUserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Appeal.objects.all()
        if self.request.user.is_municipal:
            return Appeal.objects.filter(municipal=self.request.user)
        return Appeal.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer: serializers = self.get_serializer(
            data=request.data,
            context={'user_id': request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        appeal_instance: Appeal = serializer.save()
        response_serializer: serializers = AppealUserSerializer(
            instance=appeal_instance
        )
        return Response(
            data=response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    @action(
        detail=True,
        methods=('post',),
        url_path='post_answer',
        permission_classes=(IsMunicipal,),
    )
    def post_answer(self, request, pk):
        """Оставить ответ обращению."""
        appeal: Appeal = get_object_or_404(
            Appeal,
            id=pk,
            municipal=self.request.user,
        )
        if appeal.answer is not None:
            return Response(
                data={
                    'detail': (
                        'Вы уже дали официальный ответ обращению.'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer: serializers = AppealAnswerSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        appeal.answer: float = serializer.validated_data.get('answer')
        appeal.status: str = APPEAL_STAGE_COMPLETED
        return Response(
            data={'answer': 'Ответ обращению оставлен.'},
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=('post',),
        url_path='rate_answer',
        permission_classes=(IsAuthenticated,),
    )
    def rate_answer(self, request, pk):
        """Оставить оценку ответу обращения."""
        appeal: Appeal = get_object_or_404(
            Appeal, id=pk, user=self.request.user
        )
        if appeal.status != APPEAL_STAGE_COMPLETED:
            return Response(
                data={
                    'detail': (
                        'Вы не можете поставить оценку '
                        'незавершенному обращению.'
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer: serializers = AppealRatingSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        appeal.rating = serializer.validated_data.get('rating')
        return Response(
            data={'rating': 'Благодарим за оценку ответа!'},
            status=status.HTTP_200_OK,
        )


@extend_schema(**TOKEN_OBTAIN_SCHEMA)
class CustomTokenObtainPairView(TokenObtainPairView):
    """Используется для обновления swagger к эндпоинту получения токенов."""
    pass


@extend_schema(**TOKEN_REFRESH_SCHEMA)
class CustomTokenRefreshView(TokenRefreshView):
    """Используется для обновления swagger к эндпоинту обновления токена."""
    pass


@extend_schema_view(**NEWS_SCHEMA)
class NewsViewSet(ModelViewSet):
    """ViewSet для взаимодействия с моделью новостей."""

    http_method_names = ('get', 'post',)
    queryset = News.objects.select_related(
        'category',
        'address',
        'quiz',
    ).prefetch_related(
        'picture',
        'comment',
    ).all()

    def get_permissions(self):
        if self.action == 'add_comment':
            self.permission_classes = [IsAuthenticated,]
        elif self.request.method == 'POST':
            self.permission_classes = [IsMunicipal,]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewsPostSerializer
        return NewsSerializer

    def create(self, request, *args, **kwargs):
        serializer: serializers = self.get_serializer(
            data=request.data,
            context={'municipal_id': request.user.id},
        )
        serializer.is_valid(raise_exception=True)
        news_instance: News = serializer.save()
        response_serializer: serializers = NewsSerializer(
            instance=news_instance
        )
        return Response(
            data=response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    @action(
        methods=('post',),
        detail=True,
        url_name='add_comment',
        permission_classes=(IsAuthenticated,),
    )
    def add_comment(self, request, pk):
        """Оставить комментарий к новости."""
        news: News = get_object_or_404(News, id=pk)
        serializer: serializers = NewsCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        NewsComment.objects.create(
            author=request.user,
            news=news,
            text=serializer.validated_data.get('text'),
        )
        return Response(
            data={'comment': 'Ваш комментарий опубликован!'},
            status=status.HTTP_201_CREATED,
        )


@extend_schema_view(**USERS_SCHEMA)
class UserViewSet(ModelViewSet):
    """ViewSet для взаимодействия с моделью User."""

    http_method_names = ('get', 'post',)
    queryset = User.objects.select_related('address',).all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserRegisterSerializer
        return UserFullSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAdminUser,]
        return super().get_permissions()

    def get_queryset(self):
        is_municipal: str = self.request.query_params.get('is_municipal')
        if is_municipal == 'true':
            return User.objects.select_related(
                'address',
            ).filter(
                is_staff=False,
                is_municipal=True,
            )
        return User.objects.select_related(
            'address',
        ).filter(
            is_staff=False,
            is_municipal=False,
        )
