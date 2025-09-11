from django.contrib.auth import login
from django.db.models import Q
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator

from .forms import ProductForm, CustomUserCreationForm
from .models import CustomUser, Product, Shop

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
    paginate_by = 6
    login_url = '/login/'
    redirect_field_name = 'next'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        shop_id = self.request.GET.get("shop")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |  Q(description__icontains=query)
            )
        if shop_id:
            queryset = queryset.filter(shop_id=shop_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shops"] = Shop.objects.all()
        context["q"] = self.request.GET.get("q", "")
        context["selected_shop"] = self.request.GET.get("shop", "")
        return context

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

    def get_success_url(self):
        return reverse_lazy("product_detail", kwargs={"pk": self.object.pk})

# Удаление товара (для менеджера)
class ProductDeleteView(LoginRequiredMixin, ManagerRequiredMixin, DeleteView):
    model = Product
    context_object_name = "product"
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy("products")
