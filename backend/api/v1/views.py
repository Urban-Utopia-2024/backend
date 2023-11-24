from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema_view

from api.v1.serializers import UserRegisterSerializer
from api.v1.schemas_views import USER_SCHEMA
from user.models import User


@extend_schema_view(**USER_SCHEMA)
class UserViewSet(ModelViewSet):
    """ViewSet для взаимодействия с моделью User."""

    http_method_names = ('post',)
    # http_method_names = ('get', 'post', 'patch',)
    queryset = User.objects.select_related('address',).all()

    def get_serializer_class(self):
        if self.request.method == 'post':
            return UserRegisterSerializer
        return UserRegisterSerializer
