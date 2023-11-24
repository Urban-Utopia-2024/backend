from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,
)

from api.v1.serializers import (
    NewsSerializer, UserFullSerializer, UserRegisterSerializer,
)
from api.v1.schemas_views import (
    NEWS_SCHEMA, TOKEN_OBTAIN_SCHEMA, TOKEN_REFRESH_SCHEMA, USERS_SCHEMA,
)
from info.models import News
from user.models import User


@extend_schema(**TOKEN_OBTAIN_SCHEMA)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(**TOKEN_REFRESH_SCHEMA)
class CustomTokenRefreshView(TokenRefreshView):
    pass


@extend_schema_view(**NEWS_SCHEMA)
class NewsViewSet(ModelViewSet):
    """ViewSet для взаимодействия с моделью новостей."""

    http_method_names = ('get',)
    queryset = News.objects.select_related(
        'category',
        'address',
        'quiz',
    ).prefetch_related(
        'picture',
        'comment',
    ).all()
    serializer_class = NewsSerializer


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
