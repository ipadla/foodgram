from io import BytesIO, StringIO

from django.utils.encoding import smart_text
from rest_framework import renderers

from recipes.pdfcart import PdfCart


class PdfCartRenderer(renderers.BaseRenderer):
    media_type = 'application/pdf'
    charset = None
    format = 'pdf'
    render_style = 'binary'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        buffer = BytesIO()
        report = PdfCart(buffer)
        return report.print_cart(
            ingredients=data.get('recipes_ingredients'),
            recipes=data.get('recipes')
        )


class TextCartRenderer(renderers.BaseRenderer):
    media_type = 'application/txt'
    charset = 'utf-8'
    format = 'txt'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        buffer = StringIO()
        buffer.write('Список покупок.\n\n')
        buffer.write('Выбранные рецепты:\n')

        for recipe in data.get('recipes'):
            buffer.write(f'  - {recipe.name}\n')
        buffer.write('\nНеобходимые ингредиенты:\n')

        for ingredient in data.get('recipes_ingredients'):
            buffer.write(f'  - {ingredient["ingredient__name"]}')
            buffer.write(f': {ingredient["amount__sum"]}')
            buffer.write(f' {ingredient["ingredient__measurement_unit"]}')
            buffer.write('\n')

        return smart_text(buffer.getvalue(), encoding=self.charset)
