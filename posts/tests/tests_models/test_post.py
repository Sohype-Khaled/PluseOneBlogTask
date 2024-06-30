import inspect

from django.db import models
from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from profiles.models import Profile
from ..factories import PostFactory
from ...models import Post, Category, Tag


class PostModelStructureTestCase(TestCase):

    def test_it_extends_django_db_model(self):
        self.assertTrue(issubclass(Post, models.Model))

    def test_meta_verbose_name(self):
        self.assertEqual(Post._meta.verbose_name, _("Post"))

    def test_meta_verbose_name_plural(self):
        self.assertEqual(Post._meta.verbose_name_plural, _("Posts"))

    def test_meta_ordering(self):
        self.assertEqual(Post._meta.ordering, ('created_at',))

    def test_it_has_title_field(self):
        self.assertTrue(hasattr(Post, 'title'))

    def test_title_attribute_is_instance_of_CharField(self):
        field = Post._meta.get_field('title')
        self.assertIsInstance(field, models.CharField)

    def test_title_verbose_name(self):
        field = Post._meta.get_field('title')
        self.assertEquals(field.verbose_name, _('Title'))

    def test_title_max_length(self):
        field = Post._meta.get_field('title')
        self.assertEquals(field.max_length, 255)

    def test_it_has_content_field(self):
        self.assertTrue(hasattr(Post, 'content'))

    def test_content_attribute_is_instance_of_TextField(self):
        field = Post._meta.get_field('content')
        self.assertIsInstance(field, models.TextField)

    def test_content_verbose_name(self):
        field = Post._meta.get_field('content')
        self.assertEquals(field.verbose_name, _('Content'))

    def test_it_has_author_field(self):
        self.assertTrue(hasattr(Post, 'author'))

    def test_author_attribute_is_instance_of_ForeignKey(self):
        field = Post._meta.get_field('author')
        self.assertIsInstance(field, models.ForeignKey)

    def test_author_verbose_name(self):
        field = Post._meta.get_field('author')
        self.assertEquals(field.verbose_name, _('Author'))

    def test_author_related_name(self):
        field = Post._meta.get_field('author')
        self.assertEqual('posts', field.remote_field.related_name)

    def test_author_on_delete(self):
        field = Post._meta.get_field('author')
        self.assertEquals(field.remote_field.on_delete, models.CASCADE)

    def test_author_remote_model(self):
        field = Post._meta.get_field('author')
        self.assertEquals(field.remote_field.model, Profile)

    def test_it_has_categories_field(self):
        self.assertTrue(hasattr(Post, 'categories'))

    def test_categories_attribute_is_instance_of_ManyToManyField(self):
        field = Post._meta.get_field('categories')
        self.assertIsInstance(field, models.ManyToManyField)

    def test_categories_verbose_name(self):
        field = Post._meta.get_field('categories')
        self.assertEquals(field.verbose_name, _('Categories'))

    def test_categories_related_name(self):
        field = Post._meta.get_field('categories')
        self.assertEqual('posts', field.remote_field.related_name)

    def test_categories_remote_model(self):
        field = Post._meta.get_field('categories')
        self.assertEquals(field.remote_field.model, Category)

    def test_it_has_tags_field(self):
        self.assertTrue(hasattr(Post, 'tags'))

    def test_tags_attribute_is_instance_of_ManyToManyField(self):
        field = Post._meta.get_field('tags')
        self.assertIsInstance(field, models.ManyToManyField)

    def test_tags_verbose_name(self):
        field = Post._meta.get_field('tags')
        self.assertEquals(field.verbose_name, _('Tags'))

    def test_tags_related_name(self):
        field = Post._meta.get_field('tags')
        self.assertEqual('posts', field.remote_field.related_name)

    def test_tags_remote_model(self):
        field = Post._meta.get_field('tags')
        self.assertEquals(field.remote_field.model, Tag)

    def test_it_has_created_at_field(self):
        self.assertTrue(hasattr(Post, 'created_at'))

    def test_created_at_attribute_is_instance_of_DateTimeField(self):
        field = Post._meta.get_field('created_at')
        self.assertIsInstance(field, models.DateTimeField)

    def test_created_at_verbose_name(self):
        field = Post._meta.get_field('created_at')
        self.assertEquals(field.verbose_name, _('Created At'))

    def test_created_at_has_auto_now_add(self):
        field = Post._meta.get_field('created_at')
        self.assertTrue(field.auto_now_add)

    def test_it_has_updated_at_field(self):
        self.assertTrue(hasattr(Post, 'updated_at'))

    def test_updated_at_attribute_is_instance_of_DateTimeField(self):
        field = Post._meta.get_field('updated_at')
        self.assertIsInstance(field, models.DateTimeField)

    def test_updated_at_verbose_name(self):
        field = Post._meta.get_field('updated_at')
        self.assertEquals(field.verbose_name, _('Updated At'))

    def test_updated_at_has_auto_now(self):
        field = Post._meta.get_field('updated_at')
        self.assertTrue(field.auto_now)

    def test_it_has___str___attribute(self):
        self.assertTrue(hasattr(Post, '__str__'))

    def test___str___is_callable(self):
        self.assertTrue(callable(getattr(Post, '__str__')))

    def test___str___signature(self):
        expected_signature = ['self']
        actual_signature = inspect.getfullargspec(Post.__str__)[0]
        self.assertEquals(actual_signature, expected_signature)


class PostModelStrTestCase(TestCase):
    def test_it_returns_post_title(self):
        post = PostFactory(title="Post Title")
        self.assertEquals(str(post), post.title)
