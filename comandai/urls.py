"""
URL configuration for comandai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

from comandas.api.router import router

schema_view = get_schema_view(
    openapi.Info(
        title="ComanAI API-DOC",
        default_version="v1",
        description="Documentacion de API ComandAI",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contacto@comandai.cl"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [

    path("control/", admin.site.urls),
    path("", include("comandas.urls")),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api/", include("comandas.api.router")),
    path("api/", include(router.urls)),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("pwa.urls")),
    path("", include("comensal.urls")),
    path('qr_code/', include('qr_code.urls', namespace="qr_code")),
    path("__reload__/", include("django_browser_reload.urls")),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
