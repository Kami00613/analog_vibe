from django.urls import path
from . import views

app_name = 'cameras'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('cameras/', views.camera_list, name='camera_list'),
    path('cameras/create/', views.camera_create, name='camera_create'),
    path('cameras/<int:camera_id>/', views.camera_detail, name='camera_detail'),
    path('cameras/<int:camera_id>/edit/', views.camera_edit, name='camera_edit'),
    path('cameras/<int:camera_id>/delete/', views.camera_delete, name='camera_delete'),

    path('cameras/<int:camera_id>/reviews/add/', views.add_camera_review, name='add_camera_review'),
    path('cameras/reviews/<int:review_id>/edit/', views.edit_camera_review, name='edit_camera_review'),
    path('cameras/reviews/<int:review_id>/delete/', views.delete_camera_review, name='delete_camera_review'),
]