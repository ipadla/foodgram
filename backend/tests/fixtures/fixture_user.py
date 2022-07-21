import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture(scope='session')
def password_1():
    return 'gv9zPWhb5Xr2pHq3'


@pytest.fixture(scope='session')
def password_2():
    return 'gv9zPWhb5Xr2pHq3'


@pytest.fixture(scope='session')
def password_weak():
    return '12345'


@pytest.fixture
def admin(django_user_model, password_1):
    return django_user_model.objects.create_user(
        username='TestAdmin',
        email='admin@mail.fake',
        password=password_1,
        first_name='Admin',
        last_name='User',
        role=1
    )


@pytest.fixture
def user1(django_user_model, password_1):
    return django_user_model.objects.create_user(
        username='TestUser1',
        email='user1@mail.fake',
        password=password_1,
        first_name='Common',
        last_name='User'
    )


@pytest.fixture
def user2(django_user_model, password_1):
    return django_user_model.objects.create_user(
        username='TestUser2',
        email='user2@mail.fake',
        password=password_1,
        first_name='Common',
        last_name='User'
    )


@pytest.fixture
def client_admin(admin):
    token, _ = Token.objects.get_or_create(user=admin)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return client


@pytest.fixture
def client_user1(user1):
    token, _ = Token.objects.get_or_create(user=user1)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return client


@pytest.fixture
def client_user2(user2):
    token, _ = Token.objects.get_or_create(user=user2)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return client
