from io import BytesIO, StringIO

from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipes.decorators import favorite_and_cart
from recipes.filters import IngredientsFilter, RecipesFilter
from recipes.models import (Ingredient, Recipe, RecipeFavorites,
                            RecipeIngredients, ShoppingCart)
from recipes.pagination import RecipePagination
from recipes.pdfcart import PdfCart
from recipes.permissions import IsObjectAuthor
from recipes.renderers import PdfRenderer, PlainTextRenderer
from recipes.serializers import (IngredientSerializer, RecipeSerializer,
                                 RecipeSubscriptionSerializer)
from users.models import User


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientsFilter
    lookup_field = 'id'
    pagination_class = None
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class RecipesViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = RecipesFilter
    lookup_field = 'id'
    pagination_class = RecipePagination
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    def get_permissions(self):
        permissions = self.permission_classes

        if self.action == 'create':
            permissions = [IsAuthenticated]

        if self.action in ['destroy', 'partial_update', 'update']:
            permissions = [IsObjectAuthor]

        return [permission() for permission in permissions]

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        renderer_classes=[PlainTextRenderer, PdfRenderer]
    )
    def download_shopping_cart(self, request):
        shopping_cart = request.user.shopping_cart.all()

        recipes = Recipe.objects.filter(
            id__in=shopping_cart.values_list(
                'recipe__id',
                flat=True
            )
        )

        recipes_ingredients = RecipeIngredients.objects.filter(
            recipe__in=recipes
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(Sum('amount'))

        if request.accepted_renderer.format == 'pdf':
            buffer = BytesIO()
            report = PdfCart(buffer)
            pdf = report.print_cart(
                ingredients=recipes_ingredients,
                recipes=recipes
            )

            return Response(
                data=pdf,
                content_type='application/pdf',
                headers={
                    'Content-Disposition': 'attachment; filename="Cart.pdf"'
                },
                status=status.HTTP_200_OK
            )

        buffer = StringIO()
        buffer.write('Список покупок.\n\n')
        buffer.write('Выбранные рецепты:\n')

        for recipe in recipes:
            buffer.write(f'\t - {recipe.name}\n')
        buffer.write('\nНеобходимые ингредиенты:\n')

        for ingredient in recipes_ingredients:
            buffer.write(f'\t - {ingredient["ingredient__name"]}')
            buffer.write(f': {ingredient["amount__sum"]}')
            buffer.write(f' {ingredient["ingredient__measurement_unit"]}')
            buffer.write('\n')

        return Response(
            data=buffer.getvalue(),
            content_type='text/plain,charset=utf8',
            headers={
                'Content-Disposition': 'attachment; filename="Cart.txt"'
            },
            status=status.HTTP_200_OK
        )

    @action(
        detail=True,
        methods=['delete', 'post'],
        permission_classes=[IsAuthenticated]
    )
    @favorite_and_cart(model=RecipeFavorites)
    def favorite(self, request, id=None):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['delete', 'post'],
        permission_classes=[IsAuthenticated]
    )
    @favorite_and_cart(model=ShoppingCart)
    def shopping_cart(self, request, id=None):
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SubscriptionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = RecipePagination
    permission_classes = (IsAuthenticated,)
    serializer_class = RecipeSubscriptionSerializer

    def get_queryset(self):
        return User.objects.filter(
            id__in=self.request.user.subscriber.all().values_list(
                'author__id',
                flat=True
            )
        )
