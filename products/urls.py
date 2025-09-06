from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import (RegisterView, ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView,)

urlpatterns = [
    # Аутентификация
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),

    # Товары
    path("products/", ProductListView.as_view(), name="products"),
    path("products/add/", ProductCreateView.as_view(), name="product_add"),
    path("products/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_edit"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
]
