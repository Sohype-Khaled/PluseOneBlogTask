from rest_framework import routers

from posts.views.view_api import PostViewSet

app_name = 'posts'

router = routers.SimpleRouter()
router.register('', PostViewSet, basename='posts')
urlpatterns = router.urls
