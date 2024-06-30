from django.urls import path

from posts.views.view_api import TagsListAPIView

app_name = 'tags'

urlpatterns = [
    path('', TagsListAPIView.as_view(), name='listing')
]
