import pytest

from recipes.models import Ingredient


@pytest.fixture(autouse=True, scope='package')
def ingredients(django_db_blocker):
    with django_db_blocker.unblock():
        for i in range(5):
            Ingredient.objects.create(
                name=f'яйца иволги {i}',
                measurement_unit='шт'
            )

        return Ingredient.objects.all()
