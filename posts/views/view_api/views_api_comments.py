from django.utils.translation import gettext as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from posts.filters import CommentFilterSet
from posts.models import Comment
from posts.serializers import CommentSerializer


class CommentViewSet(ViewSet):
    queryset = Comment.objects.prefetch_related('author', 'author__user')

    @swagger_auto_schema(
        operation_description="Retrieve a list of all comments",
        manual_parameters=[
            openapi.Parameter(
                name='q',
                in_=openapi.IN_QUERY,
                description="Search term for filtering comments by content",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name='author',
                in_=openapi.IN_QUERY,
                description="Filter comments by author IDs (comma-separated)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name='post',
                in_=openapi.IN_QUERY,
                description="Filter comments by post IDs (comma-separated)",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={200: CommentSerializer(many=True)},
    )
    def list(self, request):
        queryset = CommentFilterSet(request.GET, self.queryset).qs
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new comment",
        request_body=CommentSerializer,
        responses={
            201: CommentSerializer,
            401: "Unauthorized",
            422: "Unprocessable Entity",
        },
    )
    def create(self, request):
        if not request.user.is_authenticated:
            raise NotAuthenticated("User is not authenticated")
        serializer = CommentSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @swagger_auto_schema(
        operation_description="Delete a comment by its ID",
        responses={
            204: "No Content",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
        },
    )
    def destroy(self, request, pk):
        if not request.user.is_authenticated:
            raise NotAuthenticated("User is not authenticated")

        instance = get_object_or_404(self.queryset, pk=pk)
        
        if instance.author != request.user.profile:
            raise PermissionDenied(_("You do not have permission to delete this comment"))

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
