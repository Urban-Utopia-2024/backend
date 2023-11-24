from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ModelViewSet

from api.v1.serializers import CustomTokenObtainPairSerializer
from api.v1.views import CustomTokenObtainPairView, CustomTokenRefreshView, UserViewSet

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
    path('create/', CustomTokenObtainPairView.as_view(
            serializer_class=CustomTokenObtainPairSerializer,
        ), name='token_obtain_pair'
    ),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
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
