from drf_spectacular.utils import extend_schema
from rest_framework import generics

from .models import Camera, CameraBrand, CameraReview
from .serializers import CameraBrandSerializer, CameraReviewSerializer, CameraSerializer


@extend_schema(
    tags=['Cameras'],
    summary='Список брендов камер',
    description='Возвращает список брендов камер с количеством камер у каждого бренда.'
)
class CameraBrandListAPIView(generics.ListAPIView):
    queryset = CameraBrand.objects.all().order_by('name')
    serializer_class = CameraBrandSerializer


@extend_schema(
    tags=['Cameras'],
    summary='Детальная информация о бренде камеры',
    description='Возвращает один бренд камеры по id.'
)
class CameraBrandDetailAPIView(generics.RetrieveAPIView):
    queryset = CameraBrand.objects.all()
    serializer_class = CameraBrandSerializer


@extend_schema(
    tags=['Cameras'],
    summary='Список камер',
    description='Возвращает список камер AnalogVibe в JSON-формате.'
)
class CameraListAPIView(generics.ListAPIView):
    queryset = (
        Camera.objects
        .select_related('brand', 'owner')
        .prefetch_related('reviews')
        .order_by('id')
    )
    serializer_class = CameraSerializer


@extend_schema(
    tags=['Cameras'],
    summary='Детальная информация о камере',
    description='Возвращает одну камеру по id вместе с брендом, автором, фото и количеством отзывов.'
)
class CameraDetailAPIView(generics.RetrieveAPIView):
    queryset = (
        Camera.objects
        .select_related('brand', 'owner')
        .prefetch_related('reviews')
    )
    serializer_class = CameraSerializer


@extend_schema(
    tags=['Camera reviews'],
    summary='Список комментариев к камерам',
    description='Возвращает список видимых комментариев к камерам.'
)
class CameraReviewListAPIView(generics.ListAPIView):
    queryset = (
        CameraReview.objects
        .select_related('camera', 'author')
        .filter(is_visible=True)
        .order_by('-created_at')
    )
    serializer_class = CameraReviewSerializer


@extend_schema(
    tags=['Camera reviews'],
    summary='Детальная информация о комментарии к камере',
    description='Возвращает один комментарий к камере по id.'
)
class CameraReviewDetailAPIView(generics.RetrieveAPIView):
    queryset = (
        CameraReview.objects
        .select_related('camera', 'author')
        .filter(is_visible=True)
    )
    serializer_class = CameraReviewSerializer