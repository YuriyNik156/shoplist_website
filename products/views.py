from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator

from .forms import ProductForm, CustomUserCreationForm
from .models import CustomUser, Product, Shop


class RegisterView(CreateView):
    """Регистрация нового пользователя."""

    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "products/register.html"
    success_url = reverse_lazy("products")

    def form_valid(self, form):
        """Сохраняет пользователя и выполняет вход после регистрации."""
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


class CustomLoginView(LoginView):
    """Авторизация пользователя."""

    template_name = "products/login.html"

    def get_success_url(self):
        """После входа перенаправляет на список товаров."""
        return reverse_lazy("products")


class ProductListView(LoginRequiredMixin, ListView):
    """Список товаров с фильтрацией и пагинацией (для авторизованных пользователей)."""

    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 6
    login_url = "/login/"
    redirect_field_name = "next"

    def get_queryset(self):
        """Фильтрует товары по запросу и выбранному магазину."""
        queryset = super().get_queryset().order_by("id")
        query = self.request.GET.get("q")
        shop_id = self.request.GET.get("shop")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        if shop_id:
            queryset = queryset.filter(shop_id=shop_id)
        return queryset

    def get_context_data(self, **kwargs):
        """Добавляет список магазинов и параметры фильтрации в контекст."""
        context = super().get_context_data(**kwargs)
        context["shops"] = Shop.objects.all()
        context["q"] = self.request.GET.get("q", "")
        context["selected_shop"] = self.request.GET.get("shop", "")
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Детальная информация о товаре (для авторизованных пользователей)."""

    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"


class ManagerRequiredMixin(UserPassesTestMixin):
    """Миксин: доступ только для менеджеров (sales_executive)."""

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and getattr(self.request.user, "role", None) == "sales_executive"
        )


class ProductCreateView(LoginRequiredMixin, ManagerRequiredMixin, CreateView):
    """Создание товара (только для менеджеров)."""

    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("products")

    def form_valid(self, form):
        """После сохранения товара выводит сообщение об успехе."""
        response = super().form_valid(form)
        messages.success(self.request, "Товар успешно добавлен!")
        return response


class ProductUpdateView(LoginRequiredMixin, ManagerRequiredMixin, UpdateView):
    """Редактирование товара (только для менеджеров)."""

    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("products")

    def form_valid(self, form):
        """После обновления товара выводит сообщение об успехе."""
        response = super().form_valid(form)
        messages.success(self.request, "Товар успешно обновлён!")
        return response

    def get_success_url(self):
        """После обновления перенаправляет на страницу товара."""
        return reverse_lazy("product_detail", kwargs={"pk": self.object.pk})


# Удаление товара (для менеджера)


class ProductDeleteView(LoginRequiredMixin, ManagerRequiredMixin, DeleteView):
    """Удаление товара (только для менеджеров)."""

    model = Product
    context_object_name = "product"
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy("products")

    def delete(self, request, *args, **kwargs):
        """После удаления выводит сообщение об успехе."""
        messages.success(self.request, "Товар удалён!")
        return super().delete(request, *args, **kwargs)
