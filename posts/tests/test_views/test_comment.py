import inspect

from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework.viewsets import ViewSet

from posts.models import Comment
from posts.tests.factories import CommentFactory, PostFactory
from posts.tests.test_views import create_token
from posts.views.view_api import CommentViewSet
from profiles.tests.factories import UserFactory


class CommentViewSetStructureTestCase(TestCase):
    def test_it_extends_ViewSet(self):
        self.assertTrue(issubclass(CommentViewSet, ViewSet))

    def test_it_has_queryset_attribute(self):
        self.assertTrue(hasattr(CommentViewSet, 'queryset'))

    def test_queryset_is_correct_Comment_queryset(self):
        self.assertQuerysetEqual(
            CommentViewSet.queryset,
            Comment.objects.prefetch_related('author', 'author__user'))

    def test_it_has_list_attribute(self):
        self.assertTrue(hasattr(CommentViewSet, 'list'))

    def test_list_is_callable(self):
        self.assertTrue(callable(getattr(CommentViewSet, 'list')))

    def test_list_signature(self):
        expected_signature = ['self', 'request']
        actual_signature = inspect.getfullargspec(CommentViewSet.list)[0]
        self.assertEquals(actual_signature, expected_signature)

    def test_it_has_create_attribute(self):
        self.assertTrue(hasattr(CommentViewSet, 'create'))

    def test_create_is_callable(self):
        self.assertTrue(callable(getattr(CommentViewSet, 'create')))

    def test_create_signature(self):
        expected_signature = ['self', 'request']
        actual_signature = inspect.getfullargspec(CommentViewSet.create)[0]
        self.assertEquals(actual_signature, expected_signature)

    def test_it_has_destroy_attribute(self):
        self.assertTrue(hasattr(CommentViewSet, 'destroy'))

    def test_destroy_is_callable(self):
        self.assertTrue(callable(getattr(CommentViewSet, 'destroy')))

    def test_destroy_signature(self):
        expected_signature = ['self', 'request', 'pk']
        actual_signature = inspect.getfullargspec(CommentViewSet.destroy)[0]
        self.assertEquals(actual_signature, expected_signature)


class CommentViewSetListTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        CommentFactory.create_batch(10)

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("api:comments:comments-list")

    def test_it_returns_200_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_it_return_no_data_with_unavailable_search_is_not_found(self):
        response = self.client.get(f'{self.url}?q=dummy-text')
        self.assertEqual(len(response.data), 0)

    def test_it_returns_search_result_correctly(self):
        comment = CommentFactory(content="CommentContent")
        response = self.client.get(f'{self.url}?q=CommentContent')
        self.assertEquals(comment.pk, response.data[0]['id'])

    def test_it_filters_by_author(self):
        response = self.client.get(f'{self.url}?author=2')
        expected_comments = list(Comment.objects.filter(author=2).values_list('id', flat=True))
        response_comments = [comment['id'] for comment in response.data]
        self.assertListEqual(expected_comments, response_comments)

    def test_it_filters_by_post(self):
        response = self.client.get(f'{self.url}?post=2')
        expected_comments = list(Comment.objects.filter(post=2).values_list('id', flat=True))
        response_comments = [comment['id'] for comment in response.data]
        self.assertListEqual(expected_comments, response_comments)


class PostViewSetCreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post = PostFactory()
        cls.user = UserFactory()

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("api:comments:comments-list")
        self.authorization = f"Bearer {str(create_token(self.user).access_token)}"

        self.data = {
            "post": self.post.pk,
            "content": "This is a comment",
        }

    def test_it_returns_401_if_user_is_not_authenticated(self):
        response = self.client.post(self.url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_it_returns_422_with_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.authorization)
        invalid_data = self.data.copy()
        invalid_data.pop("post")
        response = self.client.post(self.url, data=invalid_data)
        self.assertEquals(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_it_returns_201_with_valid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.authorization)
        response = self.client.post(self.url, data=self.data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_it_saves_the_data_if_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.authorization)
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.data['post'], self.data['post'])
        self.assertEqual(response.data['content'], self.data['content'])

    def test_it_saves_the_request_user_profile_as_author(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.authorization)
        response = self.client.post(self.url, data=self.data)
        self.assertEquals(response.data['author']['id'], self.user.profile.id)


class CommentViewSetDestroyTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.post = PostFactory()
        cls.comment = CommentFactory(author=cls.user.profile, post=cls.post)

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("api:comments:comments-detail", args=[self.comment.pk])

        self.authorization = f"Bearer {str(create_token(self.user).access_token)}"

    def test_it_returns_401_if_user_is_not_authenticated(self):
        response = self.client.delete(self.url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_it_returns_403_if_user_is_not_the_comment_author(self):
        user = UserFactory()
        authorization = f"Bearer {str(create_token(user).access_token)}"
        self.client.credentials(HTTP_AUTHORIZATION=authorization)
        response = self.client.delete(self.url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_it_returns_404_if_comment_does_not_exist(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.authorization)
        response = self.client.delete(reverse("api:comments:comments-detail", args=[1000]))
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_it_returns_204_with_valid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.authorization)
        response = self.client.delete(self.url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.comment = CommentFactory(author=self.user.profile)

    def test_it_delete_the_request_comment(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.authorization)
        response = self.client.delete(self.url)
        self.assertEqual(Comment.objects.count(), 0)
        self.comment = CommentFactory(author=self.user.profile)
