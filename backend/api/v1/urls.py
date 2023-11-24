from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,
)

from api.v1.serializers import CustomTokenObtainPairSerializer
from api.v1.views import UserViewSet

router: DefaultRouter = DefaultRouter()

ROUTER_DATA: list[dict[str, ModelViewSet]] = [
    {'prefix': 'users', 'viewset': UserViewSet},
]

for route in ROUTER_DATA:
    router.register(
        prefix=route.get('prefix'),
        viewset=route.get('viewset'),
        basename=route.get('prefix'),
    )

token_urls = [
    path('create/', TokenObtainPairView.as_view(
            serializer_class=CustomTokenObtainPairSerializer,
        ), name='token_obtain_pair'
    ),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = [
    path('token/', include(token_urls)),
    path('', include(router.urls)),
]
