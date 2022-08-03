# Recipes

## decorators.py

favorite_and_cart(model=None)

Необходим для избежания дублирования кода в управлении избранным и списком покупок, по сути действия одинковые.

В декоратор передается модель с которой необходимо произвести действия.

Сериализатор используется всегда один и тотже.

## filters.py

IngredientsFilter - фильтр рецептов по имени

RecipesFilter:

Фильры модели для тэгов и запросов is_favorited, is_in_shopping_cart

## management/import_ingredients.py

``` bash
python manage.py import_ingredients
```

Позволяет импортировать ингредиенты из csv файла расположенного в data/ingredients.csv

## models.py

##### Ingredient
Модель ингредиента.

Сортировка по имени.

Поля: name и measurement_unit (еденица изерения)

##### Recipe
Модель рецепта

Сортировка по дате публикации вниз.


##### RecipeFavorites
Модель избранных рецептов.

Соотносит пользователя через related_name='favorite' и рецепт через related_name='favorited'
Такое соотношение должно быть уникальным

##### RecipeIngredients
Модель ингредиентов рецепта.

Ингредиент, рецепт, количество ингредиента.

Ингредиент в рецепте должен быть уникальным.

##### ShoppingCart
Модель для корзины покупок.

Соотносит пользователя через related_name='shopping_cart' и рецепт
Соотношение уникально, нельзя дважды добавлять рецепт в корзину.

## pagination.py

Пагинация с переназначением запроса ограничивающего количество результатов на странице ?limit=6

## pdfcart.py

Используя reportlab генерирует pdf со списком покупок.

## permissions.py

IsObjectAuthor - автор ли пользователь объекту? Используется при редактировании, удалении рецепта.

## renderers.py

Оба на вход принимают два словаря: список рецептов и список ингредиентов из viewsets.py/download_shopping_cart

##### PdfCartRenderer

Собирает pdf в буфер и возвращает его.

##### TextCartRenderer

Собирает в буфер текстовый документ и возвращает его.

## serializers.py

##### IngredientSerializer
Ингредиенты, только для чтения.

##### RecipeIngredientsSerializer
Ингредиенты рецепта.

to_internal_value - Преобразует ингредиент по id и записывает количество (amount) ингредиента необходимое

to_representation - делает вывод "плоским"

##### RecipeSerializer
Сериализатор рецепта.

get_is_favorited - булево значение есть ли рецепт в избранном

get_is_in_shopping_cart - булево значение есть ли рецепт в корзине покупок

to_representation - получает относительный url картинки.

##### RecipeFavoriteShoppingSerializer

readonly сериализатор рецепта с ограниченным набором полей.

##### RecipeSubscriptionSerializer
Наследуется от users.serializers.UserSerializer с добавление поля recipes.

get_recipes - метод возвращающие сериализованные рецепты, через RecipeFavoriteShoppingSerializer
в метое учитывается наличие в запросе recipes_limit, в случае его отсутствия используется значение
поумолчанию settings.RECIPES_LIMIT = 3

## viewsets.py

### IngredientsViewSet
ReadOnlyModelViewSet

Доступно всем.

Показывает ингредиенты, без пагинации.

### RecipesViewSet

ModelViewSet

Создание рецепта доступно только аутентифицированным пользователям

Удаление и редактирование - только аторам рецепта

download_shopping_cart - позволяет скачать список покупок в формате заданном заголовком Accept

favorite, shopping_cart - через декоратор @favorite_and_cart добавляют и удаляют рецепт в избранное или список покупок.

### SubscriptionViewSet

Только list.
Выводит подписки пользователя (он должен быть аутентифицирован)
