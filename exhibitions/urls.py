from django.urls import path

from . import views


app_name = 'exhibitions'


urlpatterns = [
    path('', views.exhibition_list, name='exhibition_list'),
    path('recent/', views.recent_exhibitions, name='recent_exhibitions'),

    path('create/', views.exhibition_create, name='exhibition_create'),
    path('<int:exhibition_id>/', views.exhibition_detail, name='exhibition_detail'),
    path('<int:exhibition_id>/edit/', views.exhibition_edit, name='exhibition_edit'),
    path('<int:exhibition_id>/delete/', views.exhibition_delete, name='exhibition_delete'),

    path('<int:exhibition_id>/reviews/add/', views.add_exhibition_review, name='add_exhibition_review'),
    path('reviews/<int:review_id>/edit/', views.edit_exhibition_review, name='edit_exhibition_review'),
    path('reviews/<int:review_id>/delete/', views.delete_exhibition_review, name='delete_exhibition_review'),
]