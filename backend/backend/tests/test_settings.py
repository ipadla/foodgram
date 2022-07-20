from django.conf import settings


class TestSettings:
    def test_pytest_overriden_settings(self):
        assert settings.DATABASES["default"]["ENGINE"] == "django.db.backends.sqlite3"
        assert (
            settings.DATABASES["default"]["NAME"]
            == "file:memorydb_default?mode=memory&cache=shared"
        )
        assert settings.EMAIL_BACKEND == "django.core.mail.backends.locmem.EmailBackend"

    def test_djoser_settings(self):
        assert settings.DJOSER["LOGIN_FIELD"] == "email"

    def test_drf_settings(self):
        assert settings.REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] == [
            "rest_framework.authentication.TokenAuthentication"
        ]
