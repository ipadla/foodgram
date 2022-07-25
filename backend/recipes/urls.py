from rest_framework import routers

from recipes.viewsets import IngredientsViewSet

app_name = 'recipes'

router = routers.DefaultRouter()
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = router.urls
