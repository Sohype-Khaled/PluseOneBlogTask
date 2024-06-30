import inspect

from django.db import models
from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from ..factories import CategoryFactory
from ...models import Category


class CategoryModelStructureTestCase(TestCase):
    def test_it_extends_django_db_model(self):
        self.assertTrue(issubclass(Category, models.Model))

    def test_meta_verbose_name(self):
        self.assertEqual(Category._meta.verbose_name, _("Category"))

    def test_meta_verbose_name_plural(self):
        self.assertEqual(Category._meta.verbose_name_plural, _("Categories"))

    def test_meta_ordering(self):
        self.assertEqual(Category._meta.ordering, ('id',))

    def test_it_has_name_field(self):
        self.assertTrue(hasattr(Category, 'name'))

    def test_name_attribute_is_instance_of_CharField(self):
        field = Category._meta.get_field('name')
        self.assertIsInstance(field, models.CharField)

    def test_name_verbose_name(self):
        field = Category._meta.get_field('name')
        self.assertEquals(field.verbose_name, _('Name'))

    def test_name_max_length(self):
        field = Category._meta.get_field('name')
        self.assertEquals(field.max_length, 255)

    def test_it_has_slug_field(self):
        self.assertTrue(hasattr(Category, 'slug'))

    def test_slug_attribute_is_instance_of_SlugField(self):
        field = Category._meta.get_field('slug')
        self.assertIsInstance(field, models.SlugField)

    def test_slug_verbose_name(self):
        field = Category._meta.get_field('slug')
        self.assertEquals(field.verbose_name, _('Slug'))

    def test_it_has___str___attribute(self):
        self.assertTrue(hasattr(Category, '__str__'))

    def test___str___is_callable(self):
        self.assertTrue(callable(getattr(Category, '__str__')))

    def test___str___signature(self):
        expected_signature = ['self']
        actual_signature = inspect.getfullargspec(Category.__str__)[0]
        self.assertEquals(actual_signature, expected_signature)


class CategoryModelStrTestCase(TestCase):
    def test_it_returns_category_name(self):
        category = CategoryFactory(name="Category")
        self.assertEquals(str(category), category.name)
