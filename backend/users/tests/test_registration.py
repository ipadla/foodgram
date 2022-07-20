import pytest

from tests.common import User


class TestUsersAuth:
    @pytest.mark.django_db(transaction=True)
    def test_user_registration_and_login(self, client, client_user1, password_1, password_weak, user1):
        url = '/api/users/'
        login_url = '/api/auth/token/login/'
        data = {}

        response = client_user1.post(url, data=data)
        assert response.status_code == 403, (
            f'{response.json()}'
        )

        response = client.post(url, data=data)
        assert response.status_code == 400, (
            f'{response.json()}'
        )

        data = {
            'email': '',
            'username': '',
            'password': '',
            'first_name': '',
            'last_name': ''
        }

        response = client.post(url, data=data)
        assert response.status_code == 400, (
            f'{response.json()}'
        )

        data = {
            'email': user1.email,
            'username': 'user3',
            'password': password_weak,
            'first_name': 'Firstname',
            'last_name': 'Lastname'
        }

        response = client.post(url, data=data)
        assert response.status_code == 400, (
            f'{response.json()}'
        )

        data['email'] = 'user3@mail.fake'
        response = client.post(url, data=data)
        assert response.status_code == 400, (
            f'{response.json()}'
        )

        data['password'] = password_1
        response = client.post(url, data=data)
        assert response.status_code == 201, (
            f'{response.json()}'
        )

        user = User.objects.get(email=data['email'])
        assert user.id == response.json()['id']

        login_data = {
            'email': user.email,
            'password': password_1
        }
        response = client.post(login_url, data=login_data)
        assert response.status_code == 200
