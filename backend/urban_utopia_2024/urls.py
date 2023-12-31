from django.contrib import admin
from django.urls import include, path

from api.urls import urlpatterns as api_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns)),
]
