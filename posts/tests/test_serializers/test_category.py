import inspect

from django.test import TestCase
from rest_framework import serializers

from posts.models import Category
from posts.serializers import CategorySerializer, CategoryField
from posts.tests.factories import CategoryFactory


class CategorySerializerStructureTestCase(TestCase):
    def test_it_extends_drf_ModelSerializer(self):
        self.assertTrue(issubclass(CategorySerializer, serializers.ModelSerializer))

    def test_it_meta_model_attribute_equals_to_Category(self):
        self.assertEquals(CategorySerializer.Meta.model, Category)

    def test_it_has_meta_attribute_fields(self):
        self.assertEquals(CategorySerializer.Meta.fields, '__all__')


class CategorySerializerIntegrationTestCase(TestCase):
    def setUp(self):
        self.category = CategoryFactory(name="Category", slug="category-slug")
        self.serializer = CategorySerializer(self.category)

    def test_serializer_data_contains_the_correct_keys(self):
        keys = ['id', 'name', 'slug']
        self.assertListEqual(list(self.serializer.data.keys()), keys)

    def test_serializer_data_contains_correct_values(self):
        self.assertDictEqual(self.serializer.data, {
            "id": self.category.pk,
            "name": "Category",
            "slug": "category-slug"
        })


class CategoryFieldStructureTestCase(TestCase):
    def test_it_extends_drf_RelatedField(self):
        self.assertTrue(issubclass(CategoryField, serializers.RelatedField))

    def test_it_has_to_representation_attribute(self):
        self.assertTrue(hasattr(CategoryField, 'to_representation'))

    def test_to_representation_is_callable(self):
        self.assertTrue(callable(getattr(CategoryField, 'to_representation')))

    def test_to_representation_signature(self):
        expected_signature = ['self', 'value']
        actual_signature = inspect.getfullargspec(CategoryField.to_representation)[0]
        self.assertEquals(actual_signature, expected_signature)

    def test_it_has_to_internal_value_attribute(self):
        self.assertTrue(hasattr(CategoryField, 'to_internal_value'))

    def test_to_internal_value_is_callable(self):
        self.assertTrue(callable(getattr(CategoryField, 'to_internal_value')))

    def test_to_internal_value_signature(self):
        expected_signature = ['self', 'data']
        actual_signature = inspect.getfullargspec(CategoryField.to_internal_value)[0]
        self.assertEquals(actual_signature, expected_signature)


class CategoryFieldToRepresentationTestCase(TestCase):
    def test_it_returns_serialized_data(self):
        category = CategoryFactory()
        category_serialized = CategorySerializer(category).data
        field = CategoryField(queryset=Category.objects.all())
        self.assertEqual(field.to_representation(category), category_serialized)


class CategoryFieldToInternalValueTestCase(TestCase):
    def test_it_returns_the_data_passed_to_it(self):
        category = CategoryFactory()
        field = CategoryField(queryset=Category.objects.all())
        self.assertEqual(field.to_internal_value(category.id), category.id)
