from django.urls import path
from . import views

app_name = 'presets'

urlpatterns = [
    path('', views.preset_list, name='preset_list'),
]