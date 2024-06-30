import operator
from functools import reduce

import django_filters
from django.db.models import Q
from django.utils.translation import gettext

from .models import Post, Comment


class PostFilterSet(django_filters.FilterSet):
    q = django_filters.CharFilter(method="search", label=gettext("Search"))

    class Meta:
        model = Post
        fields = ('q', 'categories', 'tags')

    def search(self, queryset, name, value):
        columns = ["title", "content"]
        q = [Q(**{f"{column}__icontains": value}) for column in columns]
        return queryset.filter(reduce(operator.or_, q))


class CommentFilterSet(django_filters.FilterSet):
    q = django_filters.CharFilter(method="search", label=gettext("Search"))

    class Meta:
        model = Comment
        fields = ('q', 'post', 'author')

    def search(self, queryset, name, value):
        return queryset.filter(content__icontains=value)
