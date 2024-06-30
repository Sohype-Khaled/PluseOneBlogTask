from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from posts.models import Tag
from posts.serializers import TagSerializer


class TagsListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('id', 'name', 'slug')
