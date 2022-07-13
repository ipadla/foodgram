import pytest

from users.models import User


class TestUsersUrls:
    @pytest.mark.django_db(transaction=True)
    def test_auth_token_login(self, client_guest, user):
        url = '/api/auth/token/login/'
        response = client_guest.post(url)

        assert response.status_code == 400, (
            '/api/auth/token/login/ without data should return 400'
        )

        data_invalid = {
            'password': 'invalid',
            'email': 'invalid'
        }

        response = client_guest.post(url, data=data_invalid)
        assert response.status_code == 400, (
            '/api/auth/token/login/ with invalid data should return 400'
        )

        # In ReDoc successfull auth shoud return 201, but Djoser return 200
        data_valid = {
            'password': '1234567',
            'email': user.email
        }
        response = client_guest.post(url, data=data_valid)
        assert response.status_code == 200, (
            'Invalid response on valid auth data'
        )
        assert 'auth_token' in response.json(), (
            'No "auth_token" in successfull login response'
        )

    @pytest.mark.django_db(transaction=True)
    def test_auth_token_logout(self, client_guest, client_user):
        url = '/api/auth/token/logout/'

        response = client_guest.post(url)
        assert response.status_code == 401

        response = client_user.post(url)
        assert response.status_code == 204

    @pytest.mark.django_db(transaction=True)
    def test_registration(self, client_guest):
        signup_url = '/api/users/'
        signin_url = '/api/auth/token/login/'

        signup_data = {
            'email': 'registry@mail.fake',
            'username': 'usernamee',
            'password': '12345FHG678',
            'first_name': 'Firstname',
            'last_name': 'Lastname'
        }

        signin_data = {
            'email': 'registry@mail.fake',
            'password': '12345FHG678'
        }

        users_before_signup = User.objects.all().count()
        response = client_guest.post(signup_url, data=signup_data)
        assert response.status_code == 201

        assert User.objects.all().count() == users_before_signup + 1

        assert 'id' in response.json()
        assert 'email' in response.json()
        assert 'username' in response.json()
        assert 'first_name' in response.json()
        assert 'last_name' in response.json()

        response = client_guest.post(signin_url, data=signin_data)
        assert response.status_code == 200, (
            'Invalid response on valid auth data'
        )
        assert 'auth_token' in response.json(), (
            'No "auth_token" in successfull login response'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_list(self, client_guest, client_user, user):
        response = client_guest.get('/api/users/')
        assert response.status_code == 200
        response = client_guest.get('/api/users/0/')
        assert response.status_code == 401
        response = client_guest.get('/api/users/me/')
        assert response.status_code == 401

        response = client_user.get('/api/users/')
        assert response.status_code == 200
        response = client_user.get('/api/users/0/')
        assert response.status_code == 404
        response = client_user.get('/api/users/me/')
        assert response.status_code == 200

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
