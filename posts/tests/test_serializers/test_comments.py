import inspect

from django.test import TestCase, RequestFactory
from rest_framework import serializers

from posts.models import Comment
from posts.serializers import CommentSerializer
from posts.tests.factories import PostFactory, CommentFactory
from profiles.serializers import AuthorField
from profiles.tests.factories import UserFactory


class CommentSerializerStructureTestCase(TestCase):
    def test_it_extends_drf_ModelSerializer(self):
        self.assertTrue(issubclass(CommentSerializer, serializers.ModelSerializer))

    def test_it_meta_model_attribute_equals_to_Comment(self):
        self.assertEquals(CommentSerializer.Meta.model, Comment)

    def test_it_has_meta_attribute_fields(self):
        self.assertTupleEqual(CommentSerializer.Meta.fields, (
            'id', 'post', 'content', 'author', 'created_at'
        ))

    def test_it_has_meta_attribute_read_only_fields(self):
        self.assertTupleEqual(CommentSerializer.Meta.read_only_fields, (
            'id', 'author', 'created_at'
        ))

    def test_author_is_instance_of_AuthorField(self):
        serializer = CommentSerializer()
        field = serializer.fields['author']
        self.assertIsInstance(field, AuthorField)

    def test_it_has_create_attribute(self):
        self.assertTrue(hasattr(CommentSerializer, 'create'))

    def test_create_is_callable(self):
        self.assertTrue(callable(getattr(CommentSerializer, 'create')))

    def test_create_signature(self):
        expected_signature = ['self', 'validated_data']
        actual_signature = inspect.getfullargspec(CommentSerializer.create)[0]
        self.assertEquals(actual_signature, expected_signature)


class CommentSerializerCreateTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.user = UserFactory()
        self.request.user = self.user

        self.post = PostFactory()

        self.data = {
            "post": self.post.id,
            "content": "Blog Post Comment",
        }

    def test_it_creates_a_comment_with_provided_data(self):
        serializer = CommentSerializer(data=self.data, context={"request": self.request})
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEquals(instance.content, self.data['content'])
        self.assertEquals(instance.author, self.user.profile)
        self.assertEquals(instance.post, self.post)


class CommentSerializerIntegrationTestCase(TestCase):
    def setUp(self):
        self.comment = CommentFactory()
        self.serializer = CommentSerializer(self.comment)

    def test_serializer_data_contains_the_correct_keys(self):
        keys = ['id', 'post', 'content', 'author', 'created_at']
        self.assertListEqual(list(self.serializer.data.keys()), keys)
