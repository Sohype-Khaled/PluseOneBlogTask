from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from posts.models import Category
from posts.serializers import CategorySerializer


class CategoriesListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('id', 'name', 'slug')
