from rest_framework import routers

from .viewsets import TagsViewSet

app_name = 'tags'

router = routers.DefaultRouter()
router.register('tags', TagsViewSet, basename='tags')

urlpatterns = router.urls
