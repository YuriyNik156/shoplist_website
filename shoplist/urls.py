from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Главная страница → редирект на логин
    path("", lambda request: redirect("login"), name="home"),

    # Приложение "products"
    path("products/", include("products.urls")),

    # Админ-панель Django
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    # Статические файлы для режима разработки
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
