from pathlib import Path
from uuid import uuid4

from django import forms
from django.core.files.storage import default_storage
from django.utils.text import get_valid_filename

from .models import Exhibition, ExhibitionPhoto, ExhibitionReview


BAD_WORDS = ['дурак', 'тупой', 'идиот']

MAX_EXHIBITION_PHOTOS = 25
MAX_PHOTO_SIZE_MB = 5
ALLOWED_IMAGE_TYPES = [
    'image/jpeg',
    'image/png',
    'image/webp',
    'image/gif',
]


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def clean(self, data, initial=None):
        single_file_clean = super().clean

        if not data:
            return []

        if isinstance(data, (list, tuple)):
            return [
                single_file_clean(file, initial)
                for file in data
            ]

        return [single_file_clean(data, initial)]


class ExhibitionForm(forms.ModelForm):
    images = MultipleFileField(
        label='Фотографии выставки',
        required=False,
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
            'multiple': True,
        }),
        help_text='Можно загрузить от 1 до 25 фото. На карточке выставки будет показано первое фото.'
    )

    class Meta:
        model = Exhibition
        fields = ['title', 'description']

        labels = {
            'title': 'Название выставки',
            'description': 'Описание',
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Например: Пленочный город',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Опишите тему выставки, настроение и визуальный стиль...',
                'class': 'form-control'
            }),
        }

    def get_delete_photo_ids(self):
        if not self.data:
            return []

        delete_ids = []

        for photo_id in self.data.getlist('delete_photo_ids'):
            try:
                delete_ids.append(int(photo_id))
            except (TypeError, ValueError):
                continue

        return delete_ids

    def clean_images(self):
        images = self.cleaned_data.get('images') or []

        if len(images) > MAX_EXHIBITION_PHOTOS:
            raise forms.ValidationError(
                f'Можно загрузить максимум {MAX_EXHIBITION_PHOTOS} фото.'
            )

        max_size_bytes = MAX_PHOTO_SIZE_MB * 1024 * 1024

        for image in images:
            if image.size > max_size_bytes:
                raise forms.ValidationError(
                    f'Файл "{image.name}" слишком большой. Максимум {MAX_PHOTO_SIZE_MB} МБ.'
                )

            content_type = getattr(image, 'content_type', '')

            if content_type not in ALLOWED_IMAGE_TYPES:
                raise forms.ValidationError(
                    f'Файл "{image.name}" должен быть картинкой: JPG, PNG, WEBP или GIF.'
                )

        return images

    def clean(self):
        cleaned_data = super().clean()

        images = cleaned_data.get('images') or []
        delete_photo_ids = self.get_delete_photo_ids()

        if self.instance and self.instance.pk:
            existing_count = (
                self.instance.photos
                .exclude(id__in=delete_photo_ids)
                .count()
            )
        else:
            existing_count = 0

        total_count = existing_count + len(images)

        if total_count < 1:
            raise forms.ValidationError('Добавьте хотя бы одно фото для выставки.')

        if total_count > MAX_EXHIBITION_PHOTOS:
            raise forms.ValidationError(
                f'В выставке может быть максимум {MAX_EXHIBITION_PHOTOS} фото.'
            )

        return cleaned_data

    def save_photos(self, exhibition):
        images = self.cleaned_data.get('images') or []
        delete_photo_ids = self.get_delete_photo_ids()

        photos_to_delete = exhibition.photos.filter(id__in=delete_photo_ids)

        for photo in photos_to_delete:
            if photo.image_path and default_storage.exists(photo.image_path):
                default_storage.delete(photo.image_path)

        photos_to_delete.delete()

        current_count = exhibition.photos.count()

        for index, image in enumerate(images, start=current_count + 1):
            original_name = get_valid_filename(image.name)
            extension = Path(original_name).suffix.lower() or '.jpg'
            file_name = f'{uuid4().hex}{extension}'
            storage_path = f'exhibitions/{file_name}'

            saved_path = default_storage.save(storage_path, image)

            ExhibitionPhoto.objects.create(
                exhibition=exhibition,
                image_path=saved_path,
                caption=f'Фото {index}',
                position=index
            )

        for index, photo in enumerate(exhibition.photos.order_by('position', 'id'), start=1):
            if photo.position != index:
                photo.position = index
                photo.caption = f'Фото {index}'
                photo.save(update_fields=['position', 'caption'])


class ExhibitionReviewForm(forms.ModelForm):
    class Meta:
        model = ExhibitionReview
        fields = ['text']

        labels = {
            'text': 'Комментарий',
        }

        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Напишите впечатление от этой подборки...',
                'class': 'form-control'
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