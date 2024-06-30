from django.utils.translation import gettext as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from posts.filters import PostFilterSet
from posts.models import Post
from posts.serializers import PostSerializer


class PostViewSet(ViewSet):
    queryset = Post.objects.prefetch_related('author', 'author__user', 'categories', 'tags')

    @swagger_auto_schema(
        operation_description="Retrieve a list of all posts",
        manual_parameters=[
            openapi.Parameter(
                name='q',
                in_=openapi.IN_QUERY,
                description="Search term for filtering posts by title or content",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name='categories',
                in_=openapi.IN_QUERY,
                description="Filter posts by category IDs (comma-separated)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name='tags',
                in_=openapi.IN_QUERY,
                description="Filter posts by tag IDs (comma-separated)",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={200: PostSerializer(many=True)})
    def list(self, request):
        queryset = PostFilterSet(request.GET, self.queryset).qs
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new post",
        request_body=PostSerializer,
        responses={
            201: PostSerializer,
            401: "Unauthorized",
            422: "Unprocessable Entity",
        })
    def create(self, request):
        if not request.user.is_authenticated:
            raise NotAuthenticated("User is not authenticated")
        serializer = PostSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @swagger_auto_schema(
        operation_description="Retrieve a post by its ID",
        responses={200: PostSerializer, 404: "Not Found"})
    def retrieve(self, request, pk):
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = PostSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a post by its ID",
        request_body=PostSerializer,
        responses={
            200: PostSerializer,
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            422: "Unprocessable Entity",
        })
    def update(self, request, pk):
        if not request.user.is_authenticated:
            raise NotAuthenticated("User is not authenticated")

        instance = get_object_or_404(self.queryset, pk=pk)

        if instance.author != request.user.profile:
            raise PermissionDenied(_("You do not have permission to edit this post"))

        serializer = PostSerializer(instance, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @swagger_auto_schema(
        operation_description="Delete a post by its ID",
        responses={
            204: "No Content",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
        })
    def destroy(self, request, pk):
        if not request.user.is_authenticated:
            raise NotAuthenticated("User is not authenticated")

        instance = get_object_or_404(self.queryset, pk=pk)

        if instance.author != request.user.profile:
            raise PermissionDenied(_("You do not have permission to delete this post"))

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
