import pytest
from rest_framework.test import APIClient


class TestUsersAuth:
    @pytest.mark.django_db()
    def test_user_login(self, client, password_1, user1):
        url = '/api/auth/token/login/'

        response = client.post(url)
        assert response.status_code == 400, (
            f'{response.json()}'
        )

        data = {
            'password': 'invalid',
            'email': 'invalid'
        }
        response = client.post(url, data=data)
        assert response.status_code == 400, (
            f'{response.json()}'
        )

        data = {
            'password': password_1,
            'email': user1.email
        }
        response = client.post(url, data=data)
        assert response.status_code == 200, (
            f'{response.json()}'
        )
        assert 'auth_token' in response.json(), (
            'No "auth_token" in successfull login response'
        )
        auth_token = response.json()['auth_token']

        logged_in_client = APIClient()
        logged_in_client.credentials(HTTP_AUTHORIZATION=f'Token {auth_token}')

        response = logged_in_client.get('/api/users/me/')
        assert response.status_code == 200
        assert 'id' in response.json()
        assert response.json()['id'] == user1.id

    @pytest.mark.django_db()
    def test_user_logout(self, client, client_user1):
        url = '/api/auth/token/logout/'

        response = client.post(url)
        assert response.status_code == 401

        response = client_user1.post(url)
        assert response.status_code == 204
