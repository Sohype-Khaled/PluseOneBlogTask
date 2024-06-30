import inspect

from django.test import TestCase, RequestFactory
from rest_framework import serializers

from posts.serializers import PostSerializer, CategoryField, TagField
from profiles.serializers import AuthorField
from profiles.tests.factories import UserFactory
from ..factories import CategoryFactory, TagFactory, PostFactory
from ...models import Post, Category, Tag


class PostSerializerStructureTestCase(TestCase):
    def test_it_extends_drf_ModelSerializer(self):
        self.assertTrue(issubclass(PostSerializer, serializers.ModelSerializer))

    def test_it_meta_model_attribute_equals_to_Post(self):
        self.assertEquals(PostSerializer.Meta.model, Post)

    def test_it_has_meta_attribute_fields(self):
        self.assertTupleEqual(PostSerializer.Meta.fields, (
            'id', 'title', 'content', 'author', 'categories', 'tags', 'created_at', 'updated_at'
        ))

    def test_it_has_meta_attribute_read_only_fields(self):
        self.assertTupleEqual(PostSerializer.Meta.read_only_fields, (
            'author', 'created_at', 'updated_at'
        ))

    def test_categories_is_instance_of_CategoryField(self):
        serializer = PostSerializer()
        field = serializer.fields['categories'].child_relation
        self.assertIsInstance(field, CategoryField)

    def test_categories_field_queryset(self):
        serializer = PostSerializer()
        field = serializer.fields['categories'].child_relation
        self.assertQuerysetEqual(field.queryset, Category.objects.all())

    def test_tags_is_instance_of_TagField(self):
        serializer = PostSerializer()
        field = serializer.fields['tags'].child_relation
        self.assertIsInstance(field, TagField)

    def test_tags_field_queryset(self):
        serializer = PostSerializer()
        field = serializer.fields['tags'].child_relation
        self.assertQuerysetEqual(field.queryset, Tag.objects.all())

    def test_author_is_instance_of_AuthorField(self):
        serializer = PostSerializer()
        field = serializer.fields['author']
        self.assertIsInstance(field, AuthorField)

    def test_it_has_create_attribute(self):
        self.assertTrue(hasattr(PostSerializer, 'create'))

    def test_create_is_callable(self):
        self.assertTrue(callable(getattr(PostSerializer, 'create')))

    def test_create_signature(self):
        expected_signature = ['self', 'validated_data']
        actual_signature = inspect.getfullargspec(PostSerializer.create)[0]
        self.assertEquals(actual_signature, expected_signature)

    def test_it_has_update_attribute(self):
        self.assertTrue(hasattr(PostSerializer, 'update'))

    def test_update_is_callable(self):
        self.assertTrue(callable(getattr(PostSerializer, 'update')))

    def test_update_signature(self):
        expected_signature = ['self', 'instance', 'validated_data']
        actual_signature = inspect.getfullargspec(PostSerializer.update)[0]
        self.assertEquals(actual_signature, expected_signature)


class PostSerializerCreateTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.user = UserFactory()
        self.request.user = self.user

        self.categories = [CategoryFactory().id for i in range(5)]
        self.tags = [TagFactory().id for i in range(5)]
        self.data = {
            "title": "Blog Post",
            "content": "Blog Post Content",
            "categories": self.categories,
            "tags": self.tags
        }

    def test_it_creates_a_post_with_provided_data(self):
        serializer = PostSerializer(data=self.data, context={"request": self.request})
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEquals(instance.title, self.data['title'])
        self.assertEquals(instance.content, self.data['content'])
        self.assertListEqual(list(instance.categories.values_list('id', flat=True)), self.data['categories'])
        self.assertListEqual(list(instance.tags.values_list('id', flat=True)), self.data['tags'])
        self.assertEquals(instance.author, self.user.profile)


class PostSerializerUpdateTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.user = UserFactory()
        self.request.user = self.user

        self.post = PostFactory()

        self.data = {
            "title": "Blog Post 2",
            "content": "Blog Post 2 Content",
            "categories": list(self.post.categories.values_list('id', flat=True)),
            "tags": list(self.post.tags.values_list('id', flat=True))
        }

    def test_it_updates_the_post_with_provided_data(self):
        serializer = PostSerializer(data=self.data, instance=self.post, context={"request": self.request})

        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEquals(instance.title, self.data['title'])
        self.assertEquals(instance.content, self.data['content'])


class PostSerializerIntegrationTestCase(TestCase):
    def setUp(self):
        self.post = PostFactory()
        self.serializer = PostSerializer(self.post)

    def test_serializer_data_contains_the_correct_keys(self):
        keys = ['id', 'title', 'content', 'author', 'categories', 'tags', 'created_at', 'updated_at']
        self.assertListEqual(list(self.serializer.data.keys()), keys)
