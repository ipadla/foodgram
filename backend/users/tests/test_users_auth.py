import pytest

from users.models import User


class TestUsersAuth:
    @pytest.mark.django_db(transaction=True)
    def test_user_registration_and_login(self, client_guest, client_user, user):
        reg_url = '/api/users/'

        assert client_guest.post(reg_url).status_code == 400, (
            f'POST {reg_url} without data should return 401'
        )

        reg_bad_data = {
            'email': 'registry',
            'username': 'usernamee',
            'password': '12345678',
            'first_name': 'Firstname',
            'last_name': 'Lastname'
        }
        response = client_guest.post(
            reg_url,
            data=reg_bad_data
        )
        assert response.status_code == 400, (
            f'POST {reg_url} with invalid data should return 401'
        )

        users_before_registration = User.objects.all().count()
        registration_valid_data = {
            'email': 'registry@mail.fake',
            'username': 'usernamee',
            'password': '12345FHG678',
            'first_name': 'Firstname',
            'last_name': 'Lastname'
        }
        response = client_guest.post(
            reg_url,
            data=registration_valid_data
        )
        assert response.status_code == 201
        assert User.objects.all().count() == users_before_registration + 1
        assert 'id' in response.json()
        assert 'email' in response.json()
        assert 'username' in response.json()
        assert 'first_name' in response.json()
        assert 'last_name' in response.json()

        # Check login process
        login_url = '/api/auth/token/login/'

        assert client_guest.post(login_url).status_code == 400, (
            f'POST {login_url} with no data should return 400 '
        )

        login_invalid_data = {
            'password': 'invalid',
            'email': 'invalid'
        }
        response = client_guest.post(login_url, data=login_invalid_data)
        assert response.status_code == 400, (
            f'Invalid data should return 400 {login_url}'
        )

        login_valid_data = {
            'password': '12345FHG678',
            'email': 'registry@mail.fake'
        }
        response = client_guest.post(login_url, data=login_valid_data)
        assert response.status_code == 200, (
            f'Valid sould return 200 {login_url}'
        )
        assert 'auth_token' in response.json(), (
            'No "auth_token" in successfull login response'
        )

    @pytest.mark.django_db(transaction=True)
    def test_user_logout(self, client_guest, client_user):
        url = '/api/auth/token/logout/'

        response = client_guest.post(url)
        assert response.status_code == 401

        response = client_user.post(url)
        assert response.status_code == 204

    @pytest.mark.django_db(transaction=True)
    def test_user_set_password(self, client_guest, client_user, user):
        url = '/api/users/set_password/'

        response = client_guest.post(url)
        assert response.status_code == 401

        valid_data = {
            'current_password': '1234567',
            'new_password': '76543sdfsdSDF21'
        }
        response = client_user.post(url, data=valid_data)
        assert response.status_code == 204
