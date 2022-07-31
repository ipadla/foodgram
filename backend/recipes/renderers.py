from django.utils.encoding import smart_text
from rest_framework import renderers


class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'application/txt'
    charset = 'utf-8'
    format = 'txt'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return smart_text(data, encoding=self.charset)


class PdfRenderer(renderers.BaseRenderer):
    media_type = 'application/pdf'
    charset = None
    format = 'pdf'
    render_style = 'binary'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data
