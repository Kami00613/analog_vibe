from django.urls import path

from accounts import api_views as accounts_api
from cameras import api_views as cameras_api
from exhibitions import api_views as exhibitions_api
from presets import api_views as presets_api


app_name = 'api'


urlpatterns = [
    path('profiles/', accounts_api.ProfileListAPIView.as_view(), name='profile_list'),
    path('profiles/<int:pk>/', accounts_api.ProfileDetailAPIView.as_view(), name='profile_detail'),

    path('camera-brands/', cameras_api.CameraBrandListAPIView.as_view(), name='camera_brand_list'),
    path('camera-brands/<int:pk>/', cameras_api.CameraBrandDetailAPIView.as_view(), name='camera_brand_detail'),

    path('cameras/', cameras_api.CameraListAPIView.as_view(), name='camera_list'),
    path('cameras/<int:pk>/', cameras_api.CameraDetailAPIView.as_view(), name='camera_detail'),

    path('camera-reviews/', cameras_api.CameraReviewListAPIView.as_view(), name='camera_review_list'),
    path('camera-reviews/<int:pk>/', cameras_api.CameraReviewDetailAPIView.as_view(), name='camera_review_detail'),

    path('presets/', presets_api.PresetListAPIView.as_view(), name='preset_list'),
    path('presets/<int:pk>/', presets_api.PresetDetailAPIView.as_view(), name='preset_detail'),

    path('preset-reviews/', presets_api.PresetReviewListAPIView.as_view(), name='preset_review_list'),
    path('preset-reviews/<int:pk>/', presets_api.PresetReviewDetailAPIView.as_view(), name='preset_review_detail'),

    path('exhibitions/', exhibitions_api.ExhibitionListAPIView.as_view(), name='exhibition_list'),
    path('exhibitions/<int:pk>/', exhibitions_api.ExhibitionDetailAPIView.as_view(), name='exhibition_detail'),

    path('exhibition-photos/', exhibitions_api.ExhibitionPhotoListAPIView.as_view(), name='exhibition_photo_list'),
    path('exhibition-photos/<int:pk>/', exhibitions_api.ExhibitionPhotoDetailAPIView.as_view(), name='exhibition_photo_detail'),

    path('exhibition-reviews/', exhibitions_api.ExhibitionReviewListAPIView.as_view(), name='exhibition_review_list'),
    path('exhibition-reviews/<int:pk>/', exhibitions_api.ExhibitionReviewDetailAPIView.as_view(), name='exhibition_review_detail'),
]