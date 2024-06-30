from django.test import TestCase
from rest_framework import filters, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from posts.models import Category
from posts.serializers import CategorySerializer
from posts.tests.factories import CategoryFactory
from posts.views.view_api import CategoriesListAPIView


class CategoriesListAPIViewStructureTestCase(TestCase):
    def test_it_extends_ListAPIView(self):
        self.assertTrue(issubclass(CategoriesListAPIView, ListAPIView))

    def test_it_has_permission_classes_attribute(self):
        self.assertTrue(hasattr(CategoriesListAPIView, 'permission_classes'))

    def test_AllowAny_in_permission_classes(self):
        self.assertIn(AllowAny, CategoriesListAPIView.permission_classes)

    def test_it_has_queryset_attribute(self):
        self.assertTrue(hasattr(CategoriesListAPIView, 'queryset'))

    def test_queryset_is_correct_Category_queryset(self):
        self.assertQuerysetEqual(CategoriesListAPIView().get_queryset(), Category.objects.all())

    def test_it_has_serializer_class_attribute(self):
        self.assertTrue(hasattr(CategoriesListAPIView, 'serializer_class'))

    def test_serializer_class_is_CategorySerializer(self):
        self.assertEquals(CategorySerializer, CategoriesListAPIView.serializer_class)

    def test_it_has_filter_backends_attribute(self):
        self.assertTrue(hasattr(CategoriesListAPIView, 'filter_backends'))

    def test_SearchFilter_in_filter_backends(self):
        self.assertIn(filters.SearchFilter, CategoriesListAPIView.filter_backends)

    def test_it_has_search_fields_attribute(self):
        self.assertTrue(hasattr(CategoriesListAPIView, 'search_fields'))

    def test_search_fields_contains_correct_search_fields(self):
        self.assertTupleEqual(CategoriesListAPIView.search_fields, ('id', 'name', 'slug'))


class CategoriesListAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("api:categories:listing")
        for i in range(20):
            CategoryFactory()

    def test_it_returns_200_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_it_return_all_the_data(self):
        response = self.client.get(self.url)
        self.assertEquals(len(response.data), 20)

    def test_it_return_no_data_with_unavailable_search_is_not_found(self):
        response = self.client.get(f'{self.url}?search=dummy-text')
        self.assertEqual(len(response.data), 0)

    def test_it_returns_search_result_correctly(self):
        category = CategoryFactory(name="TestCat", slug="test-cat")
        response = self.client.get(f'{self.url}?search=TestCat')
        self.assertEquals(category.pk, response.data[0]['id'])
