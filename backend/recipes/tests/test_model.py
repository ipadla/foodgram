import pytest

from recipes.models import Ingredient


@pytest.mark.django_db(transaction=True)
class TestIngredientsModel:
    def test_ingredient_creation(self):
        ingredient = Ingredient.objects.create(
            name='яйца иволги',
            measurement_unit='шт'
        )

        assert ingredient is not None
