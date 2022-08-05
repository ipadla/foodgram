from io import BytesIO, StringIO

from django.utils.encoding import smart_text
from rest_framework import renderers, status
from rest_framework.exceptions import NotAuthenticated

from .pdfcart import PdfCart


class PdfCartRenderer(renderers.BaseRenderer):
    ''' Рендерим pdf.

    Через буфер, чтобы небыло лишних файлов.
    Реализация в pdfcart.py через reportlab
    '''
    media_type = 'application/pdf'
    charset = None
    format = 'pdf'
    render_style = 'binary'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context.get('request').user.is_authenticated is False:
            return status.HTTP_401_UNAUTHORIZED

        if data is None:
            return status.HTTP_404_NOT_FOUND

        buffer = BytesIO()
        report = PdfCart(buffer)
        return report.print_cart(
            ingredients=data.get('recipes_ingredients'),
            recipes=data.get('recipes')
        )


class TextCartRenderer(renderers.BaseRenderer):
    ''' Рендерим txt.

    Используя буфер, дабы не плодить файлы на диске.
    '''
    media_type = 'application/txt'
    charset = 'utf-8'
    format = 'txt'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context.get('request').user.is_authenticated is False:
            return status.HTTP_401_UNAUTHORIZED

        if data is None:
            return status.HTTP_404_NOT_FOUND

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
