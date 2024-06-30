from rest_framework import routers

from posts.views.view_api import CommentViewSet

app_name = 'comments'

router = routers.SimpleRouter()
router.register('', CommentViewSet, basename='comments')
urlpatterns = router.urls
