from pathlib import Path
from uuid import uuid4

from django import forms
from django.core.files.storage import default_storage
from django.utils.text import get_valid_filename

from .models import Preset, PresetReview


BAD_WORDS = ['дурак', 'тупой', 'идиот']

MAX_PHOTO_SIZE_MB = 5
ALLOWED_IMAGE_TYPES = [
    'image/jpeg',
    'image/png',
    'image/webp',
    'image/gif',
]


class PresetForm(forms.ModelForm):
    image = forms.FileField(
        label='Фото пресета',
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
            'data-single-photo-input': 'true',
        }),
        help_text='Загрузите одно фото пресета. При редактировании новое фото заменит старое.'
    )

    class Meta:
        model = Preset
        fields = [
            'title',
            'tone',
            'description',
            'intensity',
        ]

        labels = {
            'title': 'Название пресета',
            'tone': 'Тон',
            'description': 'Описание',
            'intensity': 'Интенсивность',
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Например: Warm Grain',
                'class': 'form-control',
            }),
            'tone': forms.TextInput(attrs={
                'placeholder': 'Например: теплый, выцветший, контрастный',
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Опишите настроение, цвета, зерно и эффект пресета...',
                'class': 'form-control',
            }),
            'intensity': forms.NumberInput(attrs={
                'placeholder': 'От 0 до 100',
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.order_fields([
            'title',
            'tone',
            'description',
            'intensity',
            'image',
        ])

    def clean_intensity(self):
        intensity = self.cleaned_data.get('intensity')

        if intensity is None:
            raise forms.ValidationError('Укажите интенсивность.')

        if intensity < 0 or intensity > 100:
            raise forms.ValidationError('Интенсивность должна быть от 0 до 100.')

        return intensity

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if not image:
            if self.instance and self.instance.pk and self.instance.image_path:
                return None

            raise forms.ValidationError('Добавьте фото пресета.')

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

    def save_image(self, preset):
        image = self.cleaned_data.get('image')

        if not image:
            return

        if preset.image_path and default_storage.exists(preset.image_path):
            default_storage.delete(preset.image_path)

        original_name = get_valid_filename(image.name)
        extension = Path(original_name).suffix.lower() or '.jpg'
        file_name = f'{uuid4().hex}{extension}'
        storage_path = f'presets/{file_name}'

        saved_path = default_storage.save(storage_path, image)

        preset.image_path = saved_path
        preset.save(update_fields=['image_path'])


class PresetReviewForm(forms.ModelForm):
    class Meta:
        model = PresetReview
        fields = ['text']

        labels = {
            'text': 'Комментарий',
        }

        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Напишите, как этот пресет выглядит на кадрах...',
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