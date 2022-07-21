# Foodgram

«Продуктовый помощник». Онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин можно скачать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Backend

#### Технологии

* [Python](https://docs.python.org/3.8/) 3.8

* [Django](https://docs.djangoproject.com/en/2.2/) 2.2

* [Django Rest Framework](https://www.django-rest-framework.org/)

* [Djoser](https://djoser.readthedocs.io/)

* [Pytest](https://docs.pytest.org/), [pytest-django](https://pytest-django.readthedocs.io/)

#### Описание приложений и api

* [Api](./docs/Backend-api.md)
* [Users](./docs/Backend-users.md)

#### Запуск проекта

##### Файл конфигруации .env

```ini
SECRET_KEY='Секретный ключ для django'
DEBUG=True
```

##### В виртуальном окружении (venv) для разработки

```bash
cd ./backend
python3.8 -m venv --prompt='foodgram' venv
pip install -U pip
pip install -Ur requirements.txt
source ./venv/bin/activate
python manage.py migrate
python manage.py createsuperuser
# Далее нужно создать администратора (все поля обязательны)
python manage.py runserver
```
