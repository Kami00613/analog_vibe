from django.urls import path
from . import views

app_name = 'presets'

urlpatterns = [
    path('', views.preset_list, name='preset_list'),
    path('<int:preset_id>/', views.preset_detail, name='preset_detail'),
]