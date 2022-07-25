from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from recipes.models import Ingredients
from recipes.serializers import IngredientsSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    permission_classes = (IsAuthenticated,)
    serializer_class = IngredientsSerializer
    queryset = Ingredients.objects.all()
