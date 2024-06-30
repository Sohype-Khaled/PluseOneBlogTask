import inspect

from django.db import models
from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from profiles.models import Profile
from ..factories import CommentFactory
from ...models import Comment, Post


class CommentModelStructureTestCase(TestCase):

    def test_it_extends_django_db_model(self):
        self.assertTrue(issubclass(Comment, models.Model))

    def test_meta_verbose_name(self):
        self.assertEqual(Comment._meta.verbose_name, _("Comment"))

    def test_meta_verbose_name_plural(self):
        self.assertEqual(Comment._meta.verbose_name_plural, _("Comments"))

    def test_meta_ordering(self):
        self.assertEqual(Comment._meta.ordering, ('created_at',))

    def test_it_has_author_field(self):
        self.assertTrue(hasattr(Comment, 'author'))

    def test_author_attribute_is_instance_of_ForeignKey(self):
        field = Comment._meta.get_field('author')
        self.assertIsInstance(field, models.ForeignKey)

    def test_author_verbose_name(self):
        field = Comment._meta.get_field('author')
        self.assertEquals(field.verbose_name, _('Author'))

    def test_author_related_name(self):
        field = Comment._meta.get_field('author')
        self.assertEqual('comments', field.remote_field.related_name)

    def test_author_on_delete(self):
        field = Comment._meta.get_field('author')
        self.assertEquals(field.remote_field.on_delete, models.CASCADE)

    def test_author_remote_model(self):
        field = Comment._meta.get_field('author')
        self.assertEquals(field.remote_field.model, Profile)

    def test_it_has_post_field(self):
        self.assertTrue(hasattr(Comment, 'post'))

    def test_post_attribute_is_instance_of_ForeignKey(self):
        field = Comment._meta.get_field('post')
        self.assertIsInstance(field, models.ForeignKey)

    def test_post_verbose_name(self):
        field = Comment._meta.get_field('post')
        self.assertEquals(field.verbose_name, _('Post'))

    def test_post_related_name(self):
        field = Comment._meta.get_field('post')
        self.assertEqual('comments', field.remote_field.related_name)

    def test_post_on_delete(self):
        field = Comment._meta.get_field('post')
        self.assertEquals(field.remote_field.on_delete, models.CASCADE)

    def test_post_remote_model(self):
        field = Comment._meta.get_field('post')
        self.assertEquals(field.remote_field.model, Post)

    def test_it_has_content_field(self):
        self.assertTrue(hasattr(Comment, 'content'))

    def test_content_attribute_is_instance_of_TextField(self):
        field = Comment._meta.get_field('content')
        self.assertIsInstance(field, models.TextField)

    def test_content_verbose_name(self):
        field = Comment._meta.get_field('content')
        self.assertEquals(field.verbose_name, _('Content'))

    def test_it_has_created_at_field(self):
        self.assertTrue(hasattr(Comment, 'created_at'))

    def test_created_at_attribute_is_instance_of_DateTimeField(self):
        field = Comment._meta.get_field('created_at')
        self.assertIsInstance(field, models.DateTimeField)

    def test_created_at_verbose_name(self):
        field = Comment._meta.get_field('created_at')
        self.assertEquals(field.verbose_name, _('Created At'))

    def test_created_at_has_auto_now_add(self):
        field = Comment._meta.get_field('created_at')
        self.assertTrue(field.auto_now_add)

    def test_it_has___str___attribute(self):
        self.assertTrue(hasattr(Post, '__str__'))

    def test___str___is_callable(self):
        self.assertTrue(callable(getattr(Post, '__str__')))

    def test___str___signature(self):
        expected_signature = ['self']
        actual_signature = inspect.getfullargspec(Post.__str__)[0]
        self.assertEquals(actual_signature, expected_signature)


class CommentModelStrTestCase(TestCase):
    def test_it_returns_comment_content(self):
        comment = CommentFactory(content="Comment")
        self.assertEquals(str(comment), comment.content)
