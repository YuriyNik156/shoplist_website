from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import (
    RegisterView, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView,
    )

urlpatterns = [
    # Аутентификация
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="products/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    # Товары
    path("", ProductListView.as_view(), name="products"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("add/", ProductCreateView.as_view(), name="product_add"),
    path("<int:pk>/edit/", ProductUpdateView.as_view(), name="product_edit"),
    path("<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
]
