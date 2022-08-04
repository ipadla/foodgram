from functools import wraps

from rest_framework import status
from rest_framework.response import Response

from .serializers import RecipeFavoriteShoppingSerializer


def favorite_and_cart(model=None):
    ''' Декоратор избранного и корзины покупок.

    Используется для добаления и удаления при DELETE и POST запросе.
    Удаляет только существующее, добавляет только несуществующее.

    В качестве параметра необходимо указать целевую модель модель
    Например: @favorite_and_cart(model=RecipeFavorites)
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, id=None):
            if model is None:
                return func(self, request, id=None)

            recipe = self.get_object()

            obj = model.objects.filter(
                recipe=recipe,
                user=request.user
            )

            if request.method == 'DELETE':
                if obj.exists():
                    obj.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)

                return Response(
                    data={'detail': 'Объект не найден.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            elif request.method == 'POST':
                if obj.exists():
                    return Response(
                        data={'errors': 'Объект уже существует.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                model.objects.create(recipe=recipe, user=request.user)
                return Response(
                    data=RecipeFavoriteShoppingSerializer(recipe).data,
                    status=status.HTTP_201_CREATED
                )

            return func(self, request, id=None)
        return wrapper
    return decorator
