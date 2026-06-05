from drf_spectacular.utils import extend_schema
from rest_framework import generics

from .models import Exhibition, ExhibitionPhoto, ExhibitionReview
from .serializers import ExhibitionPhotoSerializer, ExhibitionReviewSerializer, ExhibitionSerializer


@extend_schema(
    tags=['Exhibitions'],
    summary='Список выставок',
    description='Возвращает список опубликованных виртуальных выставок.'
)
class ExhibitionListAPIView(generics.ListAPIView):
    queryset = (
        Exhibition.objects
        .select_related('curator')
        .prefetch_related('photos', 'reviews')
        .filter(is_published=True)
        .order_by('id')
    )
    serializer_class = ExhibitionSerializer


@extend_schema(
    tags=['Exhibitions'],
    summary='Детальная информация о выставке',
    description='Возвращает одну выставку по id вместе с фотографиями.'
)
class ExhibitionDetailAPIView(generics.RetrieveAPIView):
    queryset = (
        Exhibition.objects
        .select_related('curator')
        .prefetch_related('photos', 'reviews')
        .filter(is_published=True)
    )
    serializer_class = ExhibitionSerializer


@extend_schema(
    tags=['Exhibition photos'],
    summary='Список фотографий выставок',
    description='Возвращает список фотографий, прикрепленных к выставкам.'
)
class ExhibitionPhotoListAPIView(generics.ListAPIView):
    queryset = (
        ExhibitionPhoto.objects
        .select_related('exhibition')
        .order_by('exhibition_id', 'position', 'id')
    )
    serializer_class = ExhibitionPhotoSerializer


@extend_schema(
    tags=['Exhibition photos'],
    summary='Детальная информация о фотографии выставки',
    description='Возвращает одну фотографию выставки по id.'
)
class ExhibitionPhotoDetailAPIView(generics.RetrieveAPIView):
    queryset = ExhibitionPhoto.objects.select_related('exhibition')
    serializer_class = ExhibitionPhotoSerializer


@extend_schema(
    tags=['Exhibition reviews'],
    summary='Список комментариев к выставкам',
    description='Возвращает список видимых комментариев к выставкам.'
)
class ExhibitionReviewListAPIView(generics.ListAPIView):
    queryset = (
        ExhibitionReview.objects
        .select_related('exhibition', 'author')
        .filter(is_visible=True)
        .order_by('-created_at')
    )
    serializer_class = ExhibitionReviewSerializer


@extend_schema(
    tags=['Exhibition reviews'],
    summary='Детальная информация о комментарии к выставке',
    description='Возвращает один комментарий к выставке по id.'
)
class ExhibitionReviewDetailAPIView(generics.RetrieveAPIView):
    queryset = (
        ExhibitionReview.objects
        .select_related('exhibition', 'author')
        .filter(is_visible=True)
    )
    serializer_class = ExhibitionReviewSerializer