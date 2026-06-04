from django import forms

from .models import Exhibition, ExhibitionReview


BAD_WORDS = ['дурак', 'тупой', 'идиот']


class ExhibitionForm(forms.ModelForm):
    class Meta:
        model = Exhibition
        fields = ['title', 'description', 'photos_count']

        labels = {
            'title': 'Название выставки',
            'description': 'Описание',
            'photos_count': 'Количество фото',
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
            'photos_count': forms.NumberInput(attrs={
                'placeholder': 'Например: 12',
                'class': 'form-control'
            }),
        }

    def clean_photos_count(self):
        photos_count = self.cleaned_data.get('photos_count')

        if photos_count < 1:
            raise forms.ValidationError('В выставке должна быть хотя бы одна фотография.')

        return photos_count


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