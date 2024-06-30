from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Plus One Blog Task API Documentation",
        default_version='v1',
        description="Plus One Blog Task API Documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

app_name = 'api'

urlpatterns = [

    path('categories/', include('posts.urls.urls_api_categories', namespace='categories')),
    path('tags/', include('posts.urls.urls_api_tags', namespace='tags')),
    path('posts/', include('posts.urls.urls_api_posts', namespace='posts')),
    path('comments/', include('posts.urls.urls_api_comments', namespace='comments')),
    path('auth/', include('authn.urls.urls_api_auth', namespace='auth')),

    # Swagger Documentation
    path('swagger-json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
