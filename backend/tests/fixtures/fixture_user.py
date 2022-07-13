import pytest


@pytest.fixture
def superuser(django_user_model):
    return django_user_model.objects.create_superuser(
        username='TestSuperuser',
        email='superuser@mail.fake',
        password='1234567',
        role='U'
    )


@pytest.fixture
def admin(django_user_model):
    return django_user_model.objects.create_user(
        username='TestAdmin',
        email='admin@mail.fake',
        password='1234567',
        role='A'
    )


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username='TestUser',
        email='user@mail.fake',
        password='1234567',
        role='U'
    )


@pytest.fixture
def token_superuser(superuser):
    from rest_framework.authtoken.models import Token
    token, _ = Token.objects.get_or_create(user=superuser)
    return token.key


@pytest.fixture
def client_superuser(token_superuser):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token_superuser}')
    return client


@pytest.fixture
def token_admin(admin):
    from rest_framework.authtoken.models import Token
    token, _ = Token.objects.get_or_create(user=admin)
    return token.key


@pytest.fixture
def client_admin(token_admin):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token_admin}')
    return client


@pytest.fixture
def token_user(user):
    from rest_framework.authtoken.models import Token
    token, _ = Token.objects.get_or_create(user=user)
    return token.key


@pytest.fixture
def client_user(token_user):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token_user}')
    return client


@pytest.fixture
def client_guest(token_user):
    from rest_framework.test import APIClient

    return APIClient()
