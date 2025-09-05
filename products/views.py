from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .models import CustomUser, Product
from .forms import CustomUserCreationForm

# Регистрация
class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "register.html"
    success_url = reverse_lazy("products")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("products")

# Список товаров для пользователей
class ProductListView(ListView):
    model = Product
    template_name = "base.html" # Временно, позже вернуть products.html
    context_object_name = "products"

# Роль менеджера
class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in ["sales_executive", "admin"]

# Добавление товара
class ProductCreateView(LoginRequiredMixin, ManagerRequiredMixin, CreateView):
    model = Product
    fields = ["name", "description", "price", "image", "shop"]
    template_name = "product_form.html"
    success_url = reverse_lazy("products")