from django.urls import path
from . import views

app_name = 'presets'

urlpatterns = [
    path('', views.preset_list, name='preset_list'),
    path('create/', views.preset_create, name='preset_create'),
    path('<int:preset_id>/', views.preset_detail, name='preset_detail'),
    path('<int:preset_id>/edit/', views.preset_edit, name='preset_edit'),
    path('<int:preset_id>/delete/', views.preset_delete, name='preset_delete'),

    path('<int:preset_id>/reviews/add/', views.add_preset_review, name='add_preset_review'),
    path('reviews/<int:review_id>/edit/', views.edit_preset_review, name='edit_preset_review'),
    path('reviews/<int:review_id>/delete/', views.delete_preset_review, name='delete_preset_review'),
]