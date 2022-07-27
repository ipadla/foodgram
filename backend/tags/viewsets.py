from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from tags.models import Tags
from tags.serializers import TagsSerializer


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    permission_classes = (AllowAny,)
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()
