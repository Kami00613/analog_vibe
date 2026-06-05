from drf_spectacular.utils import extend_schema
from rest_framework import generics

from .models import Profile
from .serializers import ProfileSerializer


@extend_schema(
    tags=['Profiles'],
    summary='Список профилей',
    description='Возвращает список профилей пользователей AnalogVibe.'
)
class ProfileListAPIView(generics.ListAPIView):
    queryset = (
        Profile.objects
        .select_related('user')
        .order_by('id')
    )
    serializer_class = ProfileSerializer


@extend_schema(
    tags=['Profiles'],
    summary='Детальная информация о профиле',
    description='Возвращает один профиль пользователя по id.'
)
class ProfileDetailAPIView(generics.RetrieveAPIView):
    queryset = Profile.objects.select_related('user')
    serializer_class = ProfileSerializer