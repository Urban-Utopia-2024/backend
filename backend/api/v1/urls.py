from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ModelViewSet

from api.v1.serializers import CustomTokenObtainPairSerializer
from api.v1.views import (
    AppealViewSet,
    CustomAuthToken, CustomTokenObtainPairView, CustomTokenRefreshView,
    NewsViewSet, UserViewSet,
)
from urban_utopia_2024.app_data import AUTH_TOKEN, AUTH_JWT
from urban_utopia_2024.settings import AUTH_TYPE

router: DefaultRouter = DefaultRouter()

ROUTER_DATA: list[dict[str, ModelViewSet]] = [
    {'prefix': 'appeals', 'viewset': AppealViewSet},
    {'prefix': 'news', 'viewset': NewsViewSet},
    {'prefix': 'users', 'viewset': UserViewSet},
]

for route in ROUTER_DATA:
    router.register(
        prefix=route.get('prefix'),
        viewset=route.get('viewset'),
        basename=route.get('prefix'),
    )

if AUTH_TYPE == AUTH_JWT:
    token_urls = [
        path('create/', CustomTokenObtainPairView.as_view(
                serializer_class=CustomTokenObtainPairSerializer,
            ), name='token_obtain_pair'
        ),
        path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),  # noqa (E501)
    ]
elif AUTH_TYPE == AUTH_TOKEN:
    token_urls = [
        path('create/', CustomAuthToken.as_view(), name='token_obtain')
    ]

docs_urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(), name='swagger'),
]

urlpatterns = [
    path('token/', include(token_urls)),
    path('docs/', include(docs_urlpatterns)),
    path('', include(router.urls)),
]
