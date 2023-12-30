from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

# Define URL patterns for the Django project, including admin, home, user, and shop apps.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('user/', include('user.urls')),
    path('shop/', include('shop.urls')),
    path('adminpanel/', include('adminpanel.urls')),
    path('order/', include('order.urls')),
]

# Serve static and media files during development for debugging purposes.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)