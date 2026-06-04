from django import forms

from .models import Camera, CameraReview


BAD_WORDS = ['дурак', 'тупой', 'идиот']


class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = ['brand', 'name', 'year', 'description', 'is_working', 'is_rare']

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
                'class': 'form-control'
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'Например: Zenit-E',
                'class': 'form-control'
            }),
            'year': forms.NumberInput(attrs={
                'placeholder': 'Например: 1965',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Опишите камеру, её состояние и атмосферу снимков...',
                'class': 'form-control'
            }),
            'is_working': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
            'is_rare': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
        }

    def clean_year(self):
        year = self.cleaned_data.get('year')

        if year < 1800:
            raise forms.ValidationError('Год выпуска не может быть меньше 1800.')

        if year > 2035:
            raise forms.ValidationError('Год выпуска выглядит слишком большим.')

        return year


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
