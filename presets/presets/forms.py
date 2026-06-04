from django import forms

from .models import Preset, PresetReview


BAD_WORDS = ['дурак', 'тупой', 'идиот']


class PresetForm(forms.ModelForm):
    class Meta:
        model = Preset
        fields = ['title', 'tone', 'description', 'intensity', 'is_public']

        labels = {
            'title': 'Название пресета',
            'tone': 'Тон',
            'description': 'Описание',
            'intensity': 'Интенсивность',
            'is_public': 'Открытый пресет',
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Например: Warm Grain',
                'class': 'form-control'
            }),
            'tone': forms.TextInput(attrs={
                'placeholder': 'Например: теплый, выцветший, контрастный',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Опишите настроение, цвета, зерно и эффект пресета...',
                'class': 'form-control'
            }),
            'intensity': forms.NumberInput(attrs={
                'placeholder': 'От 0 до 100',
                'class': 'form-control'
            }),
        }

    def clean_intensity(self):
        intensity = self.cleaned_data.get('intensity')

        if intensity < 0 or intensity > 100:
            raise forms.ValidationError('Интенсивность должна быть от 0 до 100.')

        return intensity


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
