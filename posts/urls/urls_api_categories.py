from django.urls import path

from posts.views.view_api import CategoriesListAPIView

app_name = 'categories'

urlpatterns = [
    path('', CategoriesListAPIView.as_view(), name='listing')
]
