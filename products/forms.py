from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Product

# Регистрация пользователя с ролями
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "role")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "role": forms.Select(attrs={"class": "form-select"}),
        }

# CRUD для менеджеров
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "image", "shop"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите название товара"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Описание"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Цена"}),
            "shop": forms.TextInput(attrs={"class": "form-control", "placeholder": "Адрес магазина"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price <= 0:
            raise forms.ValidationError("Цена должна быть больше 0.")
        return price