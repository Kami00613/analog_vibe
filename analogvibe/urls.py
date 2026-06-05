from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('cameras.urls')),
    path('', include('accounts.urls')),
    path('presets/', include('presets.urls')),
    path('exhibitions/', include('exhibitions.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)