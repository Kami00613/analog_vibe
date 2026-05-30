from django.urls import path
from . import views

app_name = 'cameras'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('cameras/', views.camera_list, name='camera_list'),
]