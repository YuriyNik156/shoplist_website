from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Shop, Product, CustomUser

# Регистрация магазинов


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "address")


# Регистрация товаров


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "shop")
    search_fields = ("name",)
    list_filter = ("shop",)


# Регистрация пользователей


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("username", "email", "password", "role")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "role",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email", "username")
    ordering = ("email",)
