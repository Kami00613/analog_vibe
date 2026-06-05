from drf_spectacular.utils import extend_schema
from rest_framework import generics

from .models import Preset, PresetReview
from .serializers import PresetReviewSerializer, PresetSerializer


@extend_schema(
    tags=['Presets'],
    summary='Список пресетов',
    description='Возвращает список публичных пленочных пресетов.'
)
class PresetListAPIView(generics.ListAPIView):
    queryset = (
        Preset.objects
        .select_related('author')
        .prefetch_related('reviews')
        .filter(is_public=True)
        .order_by('id')
    )
    serializer_class = PresetSerializer


@extend_schema(
    tags=['Presets'],
    summary='Детальная информация о пресете',
    description='Возвращает один пресет по id.'
)
class PresetDetailAPIView(generics.RetrieveAPIView):
    queryset = (
        Preset.objects
        .select_related('author')
        .prefetch_related('reviews')
        .filter(is_public=True)
    )
    serializer_class = PresetSerializer


@extend_schema(
    tags=['Preset reviews'],
    summary='Список комментариев к пресетам',
    description='Возвращает список видимых комментариев к пресетам.'
)
class PresetReviewListAPIView(generics.ListAPIView):
    queryset = (
        PresetReview.objects
        .select_related('preset', 'author')
        .filter(is_visible=True)
        .order_by('-created_at')
    )
    serializer_class = PresetReviewSerializer


@extend_schema(
    tags=['Preset reviews'],
    summary='Детальная информация о комментарии к пресету',
    description='Возвращает один комментарий к пресету по id.'
)
class PresetReviewDetailAPIView(generics.RetrieveAPIView):
    queryset = (
        PresetReview.objects
        .select_related('preset', 'author')
        .filter(is_visible=True)
    )
    serializer_class = PresetReviewSerializer