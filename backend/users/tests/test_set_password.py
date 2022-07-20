import pytest


class TestUsersAuth:
    @pytest.mark.django_db(transaction=True)
    def test_user_set_password_unauthorized(self, client):
        url = '/api/users/set_password/'

        assert client.get(url).status_code == 401
        assert client.post(url).status_code == 401

    @pytest.mark.django_db(transaction=True)
    def test_user_set_password(self, client, client_user1, password_1, password_2, password_weak, user1):
        url = '/api/users/set_password/'
        data = {}

        response = client_user1.post(url, data=data)
        assert response.status_code == 400, (
            f'{response.json()}'
        )

        data = {
            'current_password': 'INVALID PASSWORD',
            'new_password': password_2
        }
        response = client_user1.post(url, data=data)
        assert response.status_code == 400, (
            f'{response.json()}'
        )

        data = {
            'current_password': password_1,
            'new_password': password_weak
        }
        response = client_user1.post(url, data=data)
        assert response.status_code == 400, (
            f'{response.json()}'
        )

        data = {
            'current_password': password_1,
            'new_password': password_2
        }
        response = client_user1.post(url, data=data)
        assert response.status_code == 204

        url = '/api/auth/token/login/'
        data = {
            'password': password_2,
            'email': user1.email
        }
        response = client.post(url, data=data)
        assert response.status_code == 200, (
            f'{response.json()}'
        )
