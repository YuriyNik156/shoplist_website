from django.contrib.auth import login
from django.db.models import Q
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView

from .forms import ProductForm, CustomUserCreationForm
from .models import CustomUser, Product

# Регистрация
class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "products/register.html"
    success_url = reverse_lazy("products")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)

# Обработка для логина пользователя
class CustomLoginView(LoginView):
    template_name = "products/login.html"

    def get_success_url(self):
        return reverse_lazy("products")

# Список товаров (для авторизованных пользователей)
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 10
    login_url = '/login/'
    redirect_field_name = 'next'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |  Q(description__icontains=query)
            )
        return queryset

# Детальное представление товара (для авторизованных пользователей)
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"

# Проверка роли менеджера
class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return (
                self.request.user.is_authenticated
                and getattr(self.request.user, "role", None) in ["sales_executive", "admin"]
        )

# Создание товара (для менеджера)
class ProductCreateView(LoginRequiredMixin, ManagerRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("products")

# Редактирование товара (для менеджера)
class ProductUpdateView(LoginRequiredMixin, ManagerRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("products")

# Удаление товара (для менеджера)
class ProductDeleteView(LoginRequiredMixin, ManagerRequiredMixin, DeleteView):
    model = Product
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy("products")