from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Product

# Регистрация пользователя с ролями
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "role")

# CRUD для менеджеров
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "image", "shop"]

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price <= 0:
            raise forms.ValidationError("Цена должна быть больше 0.")
        return price