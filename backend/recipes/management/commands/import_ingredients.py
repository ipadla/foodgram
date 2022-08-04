from csv import reader

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Import ingredients data from csv file.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Importing ingredients'))
        path = f'{settings.BASE_DIR}/data/ingredients.csv'

        with open(path) as f:
            ingredients = reader(f)
            for row in ingredients:
                _, _ = Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )
