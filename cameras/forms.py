from pathlib import Path
from uuid import uuid4

from django import forms
from django.core.files.storage import default_storage
from django.utils.text import get_valid_filename

from .models import Camera, CameraReview


BAD_WORDS = ['дурак', 'тупой', 'идиот']

MAX_PHOTO_SIZE_MB = 5
ALLOWED_IMAGE_TYPES = [
    'image/jpeg',
    'image/png',
    'image/webp',
    'image/gif',
]


class CameraForm(forms.ModelForm):
    image = forms.FileField(
        label='Фото камеры',
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
            'data-single-photo-input': 'true',
        }),
        help_text='Загрузите одно фото камеры. При редактировании новое фото заменит старое.'
    )

    class Meta:
        model = Camera
        fields = [
            'brand',
            'name',
            'year',
            'description',
            'is_working',
            'is_rare',
        ]

        labels = {
            'brand': 'Бренд',
            'name': 'Название камеры',
            'year': 'Год выпуска',
            'description': 'Описание',
            'is_working': 'Камера рабочая',
            'is_rare': 'Редкая модель',
        }

        widgets = {
            'brand': forms.Select(attrs={
                'class': 'form-control',
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'Например: Zenit-E',
                'class': 'form-control',
            }),
            'year': forms.NumberInput(attrs={
                'placeholder': 'Например: 1965',
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Опишите камеру, её состояние и атмосферу снимков...',
                'class': 'form-control',
            }),
            'is_working': forms.CheckboxInput(attrs={
                'class': 'form-checkbox',
            }),
            'is_rare': forms.CheckboxInput(attrs={
                'class': 'form-checkbox',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.order_fields([
            'brand',
            'name',
            'year',
            'description',
            'image',
            'is_working',
            'is_rare',
        ])

    def clean_year(self):
        year = self.cleaned_data.get('year')

        if year is None:
            raise forms.ValidationError('Укажите год выпуска.')

        if year < 1800:
            raise forms.ValidationError('Год выпуска не может быть меньше 1800.')

        if year > 2035:
            raise forms.ValidationError('Год выпуска выглядит слишком большим.')

        return year

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if not image:
            if self.instance and self.instance.pk and self.instance.image_path:
                return None

            raise forms.ValidationError('Добавьте фото камеры.')

        max_size_bytes = MAX_PHOTO_SIZE_MB * 1024 * 1024

        if image.size > max_size_bytes:
            raise forms.ValidationError(
                f'Файл "{image.name}" слишком большой. Максимум {MAX_PHOTO_SIZE_MB} МБ.'
            )

        content_type = getattr(image, 'content_type', '')

        if content_type not in ALLOWED_IMAGE_TYPES:
            raise forms.ValidationError(
                f'Файл "{image.name}" должен быть картинкой: JPG, PNG, WEBP или GIF.'
            )

        return image

    def save_image(self, camera):
        image = self.cleaned_data.get('image')

        if not image:
            return

        if camera.image_path and default_storage.exists(camera.image_path):
            default_storage.delete(camera.image_path)

        original_name = get_valid_filename(image.name)
        extension = Path(original_name).suffix.lower() or '.jpg'
        file_name = f'{uuid4().hex}{extension}'
        storage_path = f'cameras/{file_name}'

        saved_path = default_storage.save(storage_path, image)

        camera.image_path = saved_path
        camera.save(update_fields=['image_path'])


class CameraReviewForm(forms.ModelForm):
    class Meta:
        model = CameraReview
        fields = ['text']

        labels = {
            'text': 'Комментарий',
        }

        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Напишите, какие ощущения вызывает эта камера...',
                'class': 'form-control',
            }),
        }

    def clean_text(self):
        text = self.cleaned_data.get('text', '').strip()
        lower_text = text.lower()

        if len(text) < 5:
            raise forms.ValidationError('Комментарий должен быть не короче 5 символов.')

        for word in BAD_WORDS:
            if word in lower_text:
                raise forms.ValidationError('Комментарий содержит недопустимое слово.')

        return text