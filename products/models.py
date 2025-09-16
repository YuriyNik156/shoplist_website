from django.contrib.auth.models import AbstractUser
from django.db import models


class Shop(models.Model):
    """Модель магазина."""

    name = models.CharField(max_length=100)
    address = models.TextField(max_length=255)

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"

    def __str__(self):
        return f"{self.name} - {self.address}"


class Product(models.Model):
    """Модель товара."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="products")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name} ({self.shop})"


class CustomUser(AbstractUser):
    """Кастомная модель пользователя с email и ролью."""

    ROLE_CHOICES = [
        ('sales_executive', 'Sales Executive'),
        ('user', 'User'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} ({self.role})"

