# Сайт для публикации физических товаров и адресов магазинов (ShopList)

**Описание**

Django-приложение для управления списками покупок.

---

## Установка и настройка

1. **Клонировать репозиторий**:

   ```bash
   git clone https://github.com/ваш_пользователь/shoplist_website.git
   cd shoplist_website
   ```
   
2. **Создать виртуальное окружение и установить зависимости**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

3. **Инициализировать базу данных** (для Windows):

   ```bash
   # Выполнить команды вручную:
   python manage.py migrate
   ```
   
4. **Запустить сервер разработки**:
   
   ```bash
   python manage.py runserver
   ```

---

## Лицензия

Проект распространяется под MIT License.