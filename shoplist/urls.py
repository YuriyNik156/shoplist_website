from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", lambda request: redirect("products")),  # редирект с главной на товары
    path("", include("products.urls")),  # подключаем урлы из приложения
]
