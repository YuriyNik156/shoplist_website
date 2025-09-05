from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from . import views

urlpatterns = [
    # Аутентификация
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page=reverse_lazy("login")), name="logout"),

    # Товары
    path("products/", views.ProductListView.as_view(), name="products"),
    path("products/add/", views.ProductCreateView.as_view(), name="product_add"),
]
