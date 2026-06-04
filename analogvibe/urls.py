from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('cameras.urls', namespace='cameras')),
    path('presets/', include('presets.urls', namespace='presets')),
    path('exhibitions/', include('exhibitions.urls', namespace='exhibitions')),
    path('', include('accounts.urls', namespace='accounts')),
]