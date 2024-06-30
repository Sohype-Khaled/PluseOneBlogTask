import inspect

from django.test import TestCase
from rest_framework import serializers

from posts.models import Tag
from posts.serializers import TagSerializer, TagField
from posts.tests.factories import TagFactory


class TagSerializerStructureTestCase(TestCase):
    def test_it_extends_drf_ModelSerializer(self):
        self.assertTrue(issubclass(TagSerializer, serializers.ModelSerializer))

    def test_it_meta_model_attribute_equals_to_Tag(self):
        self.assertEquals(TagSerializer.Meta.model, Tag)

    def test_it_has_meta_attribute_fields(self):
        self.assertEquals(TagSerializer.Meta.fields, '__all__')


class TagSerializerIntegrationTestCase(TestCase):
    def setUp(self):
        self.tag = TagFactory(name="Tag", slug="tag-slug")
        self.serializer = TagSerializer(self.tag)

    def test_serializer_data_contains_the_correct_keys(self):
        keys = ['id', 'name', 'slug']
        self.assertListEqual(list(self.serializer.data.keys()), keys)

    def test_serializer_data_contains_correct_values(self):
        self.assertDictEqual(self.serializer.data, {
            "id": self.tag.pk,
            "name": "Tag",
            "slug": "tag-slug"
        })


class TagFieldStructureTestCase(TestCase):
    def test_it_extends_drf_RelatedField(self):
        self.assertTrue(issubclass(TagField, serializers.RelatedField))

    def test_it_has_to_representation_attribute(self):
        self.assertTrue(hasattr(TagField, 'to_representation'))

    def test_to_representation_is_callable(self):
        self.assertTrue(callable(getattr(TagField, 'to_representation')))

    def test_to_representation_signature(self):
        expected_signature = ['self', 'value']
        actual_signature = inspect.getfullargspec(TagField.to_representation)[0]
        self.assertEquals(actual_signature, expected_signature)

    def test_it_has_to_internal_value_attribute(self):
        self.assertTrue(hasattr(TagField, 'to_internal_value'))

    def test_to_internal_value_is_callable(self):
        self.assertTrue(callable(getattr(TagField, 'to_internal_value')))

    def test_to_internal_value_signature(self):
        expected_signature = ['self', 'data']
        actual_signature = inspect.getfullargspec(TagField.to_internal_value)[0]
        self.assertEquals(actual_signature, expected_signature)


class TagFieldToRepresentationTestCase(TestCase):
    def test_it_returns_serialized_data(self):
        tag = TagFactory()
        tag_serialized = TagSerializer(tag).data
        field = TagField(queryset=Tag.objects.all())
        self.assertEqual(field.to_representation(tag), tag_serialized)


class TagFieldToInternalValueTestCase(TestCase):
    def test_it_returns_the_data_passed_to_it(self):
        tag = TagFactory()
        field = TagField(queryset=Tag.objects.all())
        self.assertEqual(field.to_internal_value(tag.id), tag.id)
