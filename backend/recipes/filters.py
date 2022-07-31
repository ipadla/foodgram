from django_filters import filterset

from recipes.models import Ingredient, Recipe


class IngredientsFilter(filterset.FilterSet):
    name = filterset.CharFilter(method='name_filter')

    def name_filter(self, queryset, name, value):
        return Ingredient.objects.filter(name__icontains=value)


class RecipesFilter(filterset.FilterSet):
    is_favorited = filterset.CharFilter(
        label='is_favorited',
        method='recipe_favorited'
    )

    is_in_shopping_cart = filterset.CharFilter(
        label='is_in_shopping_cart',
        method='recipe_in_shopping_cart'
    )

    tags = filterset.CharFilter(
        method='recipe_tags'
    )

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']

    def recipe_favorited(self, queryset, name, value):

        if self.request.user.is_anonymous is True:
            return queryset.filter()

        if value == '1':
            # TODO: select_related/prefetch_related?
            favorites = self.request.user.favorite.all()
            return queryset.filter(
                id__in=favorites.values_list('recipe__id')
            ).distinct()

        return queryset.filter()

    def recipe_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_anonymous is True:
            return queryset.filter()

        if value == '1':
            # TODO: select_related/prefetch_related?
            shopping_cart = self.request.user.shopping_cart.all()
            return queryset.filter(
                id__in=shopping_cart.values_list('recipe__id')
            ).distinct()

        return queryset.filter()

    def recipe_tags(self, queryset, name, value):
        return queryset.filter(
            tags__slug__in=self.request.query_params.getlist(name)
        ).distinct()
