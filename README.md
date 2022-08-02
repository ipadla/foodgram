# Foodgram

«Продуктовый помощник». Онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин можно скачать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Демо проекта

Демо проекта доступно по адресу http://foodgram.ipadla.org

Докуменация к API [http://foodgram.ipadla.org/api/docs/](http://foodgram.ipadla.org/api/docs/)

Созданы пользователи

| login | email           | password  |
| ----- | --------------- | --------- |
| admin | admin@mail.fake | 123123qaz |
| moder | moder@mail.fake | 123123qaz |
| user  | user@mail.fake  | 123123qaz |

## Backend

В рамках дипломного проекта реализован.

#### Технологии

* [Python](https://docs.python.org/3.8/) 3.8
* [Django](https://docs.djangoproject.com/en/2.2/) 2.2
* django-filter
* gunicorn
* [Django Rest Framework](https://www.django-rest-framework.org/)
* [Djoser](https://djoser.readthedocs.io/)
* [Pytest](https://docs.pytest.org/), [pytest-django](https://pytest-django.readthedocs.io/)

#### Описание приложений и api

* [Api](./docs/Backend-api.md)
* [Users](./docs/Backend-users.md)

#### Запуск проекта

##### Файл конфигруации .env

Файл конфигурации должен находиться в папке infra

Django использует python-dotenv для загрузки файла в процессе разработки, при деплое на сервер этот же файл используется для задания переменных окружения контейнера.

```ini
SECRET_KEY='Секретный ключ для django'
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

##### Для разработки

Подготовлен специальный *docker-compose-dev.yml* запускающий контейнеры db, frontend и nginx

для nginx контейнера созданы специальные настройки, позволяющие nginx обращаться к хосту через host.containers.internal

В конфигурационный файл .env селдует добавить строку **DEBUG=True** и изменить на *localhost*, либо удалить ключ **DB_HOST**

Для запуска:

```bash
cd infra
podman-compose -f ./docker-compose-dev.yml up
```

Далее запускается виртуальное окружение Python:

```bash
cd ./backend
python3.8 -m venv --prompt='foodgram' venv
pip install -U pip
pip install -Ur requirements.txt
source ./venv/bin/activate
python manage.py migrate
```

Создание суперпользователя:

```bash
python manage.py createsuperuser
```

Если необходимо - загрузка тестовых данных:

```bash
python manage.py loaddata ./data/fixtures.json
```

Запуск сервера разработки:

```bash
python manage.py runserver 0.0.0.0:8000
```

##### Для общего доступа

```bash
cd ./backend
podman-compose up --build
podman-compose exec backend python manage.py collectstatic --no-input
podman-compose exec backend python manage.py migrate
```

Далее по желанию:

Создание суперпользователя:

```bash
podman-compose exec backendpython manage.py createsuperuser
```

Загрузка тестовых данных:

```bash
podman-compose exec backend python manage.py loaddata \
/app/data/fixtures.json
```


