from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Product, Shop

User = get_user_model()

# Проверка создания магазина и связанного с ним товара
class ProductModelTest(TestCase):
    def test_create_product(self):
        shop = Shop.objects.create(
            name="Магазин №1",
            address="ул. Ленина, 1"
        )
        product = Product.objects.create(
            name="Тестовый товар",
            description="Описание товара",
            price=100.50,
            shop=shop
        )
        self.assertEqual(product.name, "Тестовый товар")
        self.assertEqual(product.shop.name, "Магазин №1")
        self.assertEqual(Product.objects.count(), 1)


# Проверка создания кастомного пользователя
class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpass",
            role="user"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.role, "user")
        self.assertTrue(user.check_password("testpass"))


# создание ролей (администратор, менеджер, пользователь)
class ViewsAccessTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="adminpass",
            role="admin"
        )
        self.manager = User.objects.create_user(
            username="manager",
            email="manager@test.com",
            password="managerpass",
            role="sales_executive"
        )
        self.user = User.objects.create_user(
            username="user",
            email="user@test.com",
            password="userpass",
            role="user"
        )

        # Создание магазина от имени администратора
        self.shop = Shop.objects.create(
            name="Магазин №1",
            address="ул. Ленина, 1"
        )

        # Создание тестового товара
        self.product = Product.objects.create(
            name="Старый товар",
            description="Описание",
            price=100,
            shop=self.shop
        )

    # Неавторизованный посетитель при попытке зайти на список товаров получает редирект на логин
    def test_visitor_redirects_to_login(self):
        response = self.client.get(reverse("products"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    # Обычный пользователь после логина может просматривать список товаров
    def test_user_can_view_products(self):
        self.client.login(email="user@test.com", password="userpass")
        response = self.client.get(reverse("products"))
        self.assertEqual(response.status_code, 200)

    # Администратор может добавить товар в магазин
    def test_admin_can_add_product(self):
        self.client.login(email="admin@test.com", password="adminpass")
        response = self.client.post(
            reverse("product_add"),
            {
                "name": "Новый товар от админа",
                "description": "Описание",
                "price": "199.99",
                "shop": self.shop.id,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 2)

    # Менеджер может добавить товар в магазин
    def test_manager_can_add_product(self):
        self.client.login(email="manager@test.com", password="managerpass")
        response = self.client.post(
            reverse("product_add"),
            {
                "name": "Новый товар от менеджера",
                "description": "Описание",
                "price": "299.99",
                "shop": self.shop.id,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 2)

    # Обычный пользователь не может добавить товар (ошибка 403)
    def test_user_cannot_add_product(self):
        self.client.login(email="user@test.com", password="userpass")
        response = self.client.post(
            reverse("product_add"),
            {
                "name": "Попытка от пользователя",
                "description": "Описание",
                "price": "399.99",
                "shop": self.shop.id,
            }
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Product.objects.count(), 1)

    # Администратор может редактировать товар
    def test_admin_can_edit_product(self):
        self.client.login(email="admin@test.com", password="adminpass")
        response = self.client.post(
            reverse("product_edit", args=[self.product.id]),
            {
                "name": "Изменённый товар",
                "description": "Новое описание",
                "price": "500",
                "shop": self.shop.id,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Изменённый товар")

    # Менеджер может редактировать товар
    def test_manager_can_edit_product(self):
        self.client.login(email="manager@test.com", password="managerpass")
        response = self.client.post(
            reverse("product_edit", args=[self.product.id]),
            {
                "name": "Менеджер изменил товар",
                "description": "Новое описание",
                "price": "600",
                "shop": self.shop.id,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Менеджер изменил товар")

    # Обычный пользователь не может редактировать товар (ошибка 403)
    def test_user_cannot_edit_product(self):
        self.client.login(email="user@test.com", password="userpass")
        response = self.client.post(
            reverse("product_edit", args=[self.product.id]),
            {
                "name": "Попытка изменить",
                "description": "Не должно сработать",
                "price": "700",
                "shop": self.shop.id,
            }
        )
        self.assertEqual(response.status_code, 403)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Старый товар")


    # Администратор может удалить товар
    def test_admin_can_delete_product(self):
        self.client.login(email="admin@test.com", password="adminpass")
        response = self.client.post(reverse("product_delete", args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 0)

    # Менеджер может удалить товар
    def test_manager_can_delete_product(self):
        self.client.login(email="manager@test.com", password="managerpass")
        response = self.client.post(reverse("product_delete", args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 0)

    # Обычный пользователь не может удалить товар (ошибка 403)
    def test_user_cannot_delete_product(self):
        self.client.login(email="user@test.com", password="userpass")
        response = self.client.post(reverse("product_delete", args=[self.product.id]))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Product.objects.count(), 1)