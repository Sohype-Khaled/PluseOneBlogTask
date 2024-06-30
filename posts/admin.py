from django.contrib import admin
from django.utils.translation import gettext as _

from .models import Category, Post, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (_("Details"), {
            'fields': ['title', 'content', "author"],
        }),
        (_("Classifications"), {
            'fields': [('categories', 'tags')],
        }),
    ]
    list_display = ('id', 'title', 'author', 'created_at')
    list_display_links = ['title']
    list_filter = ('categories', 'tags')
    search_fields = ('title', 'content',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug"]
    fields = (("name", "slug"),)
    list_display_links = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug"]
    fields = (("name", "slug"),)
    list_display_links = ['name']
