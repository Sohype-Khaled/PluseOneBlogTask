import inspect

from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework.viewsets import ViewSet

from posts.views.view_api import PostViewSet
from ..factories import PostFactory
from ...models import Post


class PostViewSetStructureTestCase(TestCase):
    def test_it_extends_ViewSet(self):
        self.assertTrue(issubclass(PostViewSet, ViewSet))

    def test_it_has_queryset_attribute(self):
        self.assertTrue(hasattr(PostViewSet, 'queryset'))

    def test_queryset_is_correct_Category_queryset(self):
        self.assertQuerysetEqual(
            PostViewSet.queryset,
            Post.objects.prefetch_related('author', 'author__user', 'categories', 'tags'))

    def test_it_has_list_attribute(self):
        self.assertTrue(hasattr(PostViewSet, 'list'))

    def test_list_is_callable(self):
        self.assertTrue(callable(getattr(PostViewSet, 'list')))

    def test_list_signature(self):
        expected_signature = ['self', 'request']
        actual_signature = inspect.getfullargspec(PostViewSet.list)[0]
        self.assertEquals(actual_signature, expected_signature)

    def test_it_has_create_attribute(self):
        self.assertTrue(hasattr(PostViewSet, 'create'))

    def test_create_is_callable(self):
        self.assertTrue(callable(getattr(PostViewSet, 'create')))

    def test_create_signature(self):
        expected_signature = ['self', 'request']
        actual_signature = inspect.getfullargspec(PostViewSet.create)[0]
        self.assertEquals(actual_signature, expected_signature)

    def test_it_has_retrieve_attribute(self):
        self.assertTrue(hasattr(PostViewSet, 'retrieve'))

    def test_retrieve_is_callable(self):
        self.assertTrue(callable(getattr(PostViewSet, 'retrieve')))

    def test_retrieve_signature(self):
        expected_signature = ['self', 'request', 'pk']
        actual_signature = inspect.getfullargspec(PostViewSet.retrieve)[0]
        self.assertEquals(actual_signature, expected_signature)

    def test_it_has_update_attribute(self):
        self.assertTrue(hasattr(PostViewSet, 'update'))

    def test_update_is_callable(self):
        self.assertTrue(callable(getattr(PostViewSet, 'update')))

    def test_update_signature(self):
        expected_signature = ['self', 'request', 'pk']
        actual_signature = inspect.getfullargspec(PostViewSet.update)[0]
        self.assertEquals(actual_signature, expected_signature)

    def test_it_has_destroy_attribute(self):
        self.assertTrue(hasattr(PostViewSet, 'destroy'))

    def test_destroy_is_callable(self):
        self.assertTrue(callable(getattr(PostViewSet, 'destroy')))

    def test_destroy_signature(self):
        expected_signature = ['self', 'request', 'pk']
        actual_signature = inspect.getfullargspec(PostViewSet.destroy)[0]
        self.assertEquals(actual_signature, expected_signature)


class PostViewSetListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("api:posts:listing")
        for i in range(20):
            PostFactory()

# self.user = UserFactory()
# self.authorization = f"Bearer {str(create_token(self.user).access_token)}"
