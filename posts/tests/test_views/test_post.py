import inspect

from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework.viewsets import ViewSet

from posts.views.view_api import PostViewSet
from profiles.tests.factories import UserFactory
from . import create_token
from ..factories import PostFactory, CategoryFactory, TagFactory
from ...models import Post, Tag, Category
from ...serializers import PostSerializer


class PostViewSetStructureTestCase(TestCase):
    def test_it_extends_ViewSet(self):
        self.assertTrue(issubclass(PostViewSet, ViewSet))

    def test_it_has_queryset_attribute(self):
        self.assertTrue(hasattr(PostViewSet, 'queryset'))

    def test_queryset_is_correct_Post_queryset(self):
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
    @classmethod
    def setUpTestData(cls):
        CategoryFactory.create_batch(5)
        TagFactory.create_batch(5)
        for i in range(5):
            categories = Category.objects.filter(pk=i)
            tags = Tag.objects.filter(pk=i)
            PostFactory.create_batch(10, tags=tags, categories=categories)

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("api:posts:posts-list")

    def test_it_returns_200_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_it_returns_paginated_response(self):
        response = self.client.get(self.url)
        self.assertEquals(len(response.data['results']), 20)

    def test_it_returns_the_passed_value_of_limit(self):
        response = self.client.get(f"{self.url}?limit=5")
        self.assertEquals(len(response.data['results']), 5)

    def test_it_returns_the_expected_data_for_offset(self):
        response = self.client.get(f"{self.url}?offset=5")
        expected_ids = list(Post.objects.all()[5:25].values_list('id', flat=True))
        response_ids = [post['id'] for post in response.data['results']]
        self.assertListEqual(expected_ids, response_ids)

    def test_it_return_no_data_with_unavailable_search_is_not_found(self):
        response = self.client.get(f'{self.url}?q=dummy-text')
        self.assertEqual(response.data['count'], 0)

    def test_it_returns_search_result_correctly(self):
        post = PostFactory(title="New Article")
        response = self.client.get(f'{self.url}?q=New Article')
        self.assertEquals(post.pk, response.data['results'][0]['id'])

    def test_it_filters_by_categories(self):
        response = self.client.get(f'{self.url}?categories=2')
        expected_posts = list(Post.objects.filter(categories=2).values_list('id', flat=True))
        response_posts = [post['id'] for post in response.data['results']]
        self.assertListEqual(expected_posts, response_posts)

    def test_it_filters_by_tags(self):
        response = self.client.get(f'{self.url}?tags=2')
        expected_posts = list(Post.objects.filter(tags=2).values_list('id', flat=True))
        response_posts = [post['id'] for post in response.data['results']]
        self.assertListEqual(expected_posts, response_posts)


class PostViewSetCreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.categories = CategoryFactory.create_batch(2)
        cls.tags = TagFactory.create_batch(2)

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("api:posts:posts-list")
        self.user = UserFactory()
        self.authorization = f"Bearer {str(create_token(self.user).access_token)}"

        self.data = {
            "title": "Blog Post 2",
            "content": "Blog Post 2 Content",
            "categories": [cat.id for cat in self.categories],
            "tags": [tag.id for tag in self.tags]
        }

    def test_it_returns_401_if_user_is_not_authenticated(self):
        response = self.client.post(self.url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_it_returns_422_with_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.authorization)
        invalid_data = self.data.copy()
        invalid_data.pop("title")
        response = self.client.post(self.url, data=invalid_data)
        self.assertEquals(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_it_returns_201_with_valid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.authorization)
        response = self.client.post(self.url, data=self.data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_it_saves_the_data_if_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.authorization)
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.data['title'], self.data['title'])
        self.assertEqual(response.data['content'], self.data['content'])
        self.assertListEqual([cat['id'] for cat in response.data['categories']], self.data['categories'])
        self.assertListEqual([tag['id'] for tag in response.data['tags']], self.data['tags'])

    def test_it_saves_the_request_user_profile_as_author(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.authorization)
        response = self.client.post(self.url, data=self.data)
        self.assertEquals(response.data['author']['id'], self.user.profile.id)


class PostViewSetRetrieveTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.categories = CategoryFactory.create_batch(2)
        cls.tags = TagFactory.create_batch(2)
        cls.post = PostFactory(tags=cls.tags, categories=cls.categories)

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("api:posts:posts-detail", args=[self.post.pk])

    def test_it_returns_200_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_it_returns_404_if_post_does_not_exist(self):
        response = self.client.get(reverse("api:posts:posts-detail", args=[1000]))
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_it_returns_the_requested_post(self):
        response = self.client.get(self.url)
        self.assertEquals(response.data['id'], self.post.id)

    def test_it_returns_correct_serializer_data(self):
        response = self.client.get(self.url)
        post_serialized = PostSerializer(self.post).data
        self.assertDictEqual(response.data, post_serialized)


class PostViewSetUpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.categories = CategoryFactory.create_batch(2)
        cls.tags = TagFactory.create_batch(2)
        cls.user = UserFactory()
        cls.post = PostFactory(tags=cls.tags, categories=cls.categories, author=cls.user.profile)

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("api:posts:posts-detail", args=[self.post.pk])

        self.authorization = f"Bearer {str(create_token(self.user).access_token)}"

        self.data = {
            "title": "Blog Post 2",
            "content": "Blog Post 2 Content",
            "categories": [cat.id for cat in self.categories],
            "tags": [tag.id for tag in self.tags]
        }

    def test_it_returns_401_if_user_is_not_authenticated(self):
        response = self.client.put(self.url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_it_returns_403_if_user_is_not_the_post_author(self):
        user = UserFactory()
        authorization = f"Bearer {str(create_token(user).access_token)}"
        self.client.credentials(HTTP_AUTHORIZATION=authorization)
        response = self.client.put(self.url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_it_returns_404_if_post_does_not_exist(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.authorization)
        response = self.client.put(reverse("api:posts:posts-detail", args=[1000]), data=self.data)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_it_returns_422_with_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.authorization)
        invalid_data = self.data.copy()
        invalid_data.pop("title")
        response = self.client.put(self.url, data=invalid_data)
        self.assertEquals(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_it_returns_200_with_valid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.authorization)
        response = self.client.put(self.url, data=self.data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_it_saves_the_data_if_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.authorization)
        response = self.client.put(self.url, data=self.data)
        self.assertEqual(response.data['title'], self.data['title'])
        self.assertEqual(response.data['content'], self.data['content'])
        self.assertListEqual([cat['id'] for cat in response.data['categories']], self.data['categories'])
        self.assertListEqual([tag['id'] for tag in response.data['tags']], self.data['tags'])


class PostViewSetDestroyTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.post = PostFactory(author=cls.user.profile)

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("api:posts:posts-detail", args=[self.post.pk])

        self.authorization = f"Bearer {str(create_token(self.user).access_token)}"

    def test_it_returns_401_if_user_is_not_authenticated(self):
        response = self.client.delete(self.url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_it_returns_403_if_user_is_not_the_post_author(self):
        user = UserFactory()
        authorization = f"Bearer {str(create_token(user).access_token)}"
        self.client.credentials(HTTP_AUTHORIZATION=authorization)
        response = self.client.delete(self.url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_it_returns_404_if_post_does_not_exist(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.authorization)
        response = self.client.delete(reverse("api:posts:posts-detail", args=[1000]))
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_it_returns_204_with_valid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.authorization)
        response = self.client.delete(self.url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.post = PostFactory(author=self.user.profile)

    def test_it_delete_the_request_post(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.authorization)
        response = self.client.delete(self.url)
        self.assertEqual(Post.objects.count(), 0)
        self.post = PostFactory(author=self.user.profile)

