from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate

styles = getSampleStyleSheet()
styles['Normal'].fontName = 'Terminus'
styles['Heading1'].fontName = 'Terminus'
styles['Heading2'].fontName = 'Terminus'

registerFont(
    TTFont('Terminus', f'{settings.BASE_DIR}/data/Terminus.ttf', 'UTF-8')
)


class PdfCart:
    def __init__(self, buffer):
        self.buffer = buffer
        self.pagesize = A4
        self.width, self.height = self.pagesize

    @staticmethod
    def _footer(canvas, doc):
        # Футер на все страницы
        canvas.saveState()

        footer = Paragraph(
            'Сгенерировано сервисом foodgram.ipadla.org',
            styles['Normal']
        )

        _, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)

        canvas.restoreState()

    def print_cart(self, recipes, ingredients):
        # Пишем список покупок в буфер.

        if recipes is None or ingredients is None:
            return

        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=72,
                                leftMargin=72,
                                topMargin=25,
                                bottomMargin=72,
                                pagesize=self.pagesize)

        elements = []
        elements.append(Paragraph(u'Список покупок', styles['Heading1']))
        elements.append(Paragraph(u'Выбранные рецепты:', styles['Heading2']))

        for recipe in recipes:
            elements.append(Paragraph(recipe.name, styles['Normal']))

        elements.append(
            Paragraph(u'Необходимые ингредиенты:', styles['Heading2'])
        )

        for ingredient in ingredients:
            elements.append(
                Paragraph(
                    (
                        f'{ingredient["ingredient__name"]} - '
                        f'{ingredient["amount__sum"]} '
                        f'{ingredient["ingredient__measurement_unit"]}'
                    ),
                    styles['Normal']
                )
            )

        doc.build(
            elements,
            onFirstPage=self._footer,
            onLaterPages=self._footer
        )

        return buffer.getvalue()
