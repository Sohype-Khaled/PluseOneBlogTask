from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import gettext as _

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include("blog.urls.urls_api", namespace="api"))
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.index_title = _("Plus One Blog Task")
admin.site.site_header = _("Plus One Blog Task")
admin.site.site_title = _("Blog Admin")
