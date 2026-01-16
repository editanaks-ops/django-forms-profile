
# Django Forms & Profile App

Учебный проект на Django: регистрация, авторизация, профиль пользователя и отправка сообщений.

## Возможности

Регистрация пользователя

Вход / выход из системы

Профиль пользователя

Отправка сообщений через форму

Хранение сообщений в базе данных

Валидация форм

## Установка

```bash
git clone https://github.com/editanaks-ops/django-forms-profile.git
cd django-forms-profile
python -m venv venv
venv\Scripts\activate
pip install django
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
Открой в браузере:
http://127.0.0.1:8000/

Страницы

/register/  регистрация

/login/  вход

/profile/ профиль пользователя

/message/  форма сообщения