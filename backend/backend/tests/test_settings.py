from django.conf import settings


class TestSettings:
    def test_djoser_settings(self):
        assert settings.DJOSER["LOGIN_FIELD"] == "email"

    def test_drf_settings(self):
        assert settings.REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] == [
            "rest_framework.authentication.TokenAuthentication"
        ]
