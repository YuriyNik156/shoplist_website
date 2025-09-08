from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import (
    RegisterView, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView,
    CustomLoginView
    )

urlpatterns = [
    # Аутентификация
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),

    # Товары
    path("", ProductListView.as_view(), name="products"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("add/", ProductCreateView.as_view(), name="product_add"),
    path("<int:pk>/edit/", ProductUpdateView.as_view(), name="product_edit"),
    path("<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
]
