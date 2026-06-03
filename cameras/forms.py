from django import forms
from .models import CameraReview


class CameraReviewForm(forms.ModelForm):
    class Meta:
        model = CameraReview
        fields = ['author_name', 'text', 'rating']

        labels = {
            'author_name': 'Ваше имя',
            'text': 'Комментарий',
            'rating': 'Оценка',
        }

        widgets = {
            'author_name': forms.TextInput(attrs={
                'placeholder': 'Например: Лена',
                'style': 'width: 100%; max-width: 420px; padding: 10px; border: 1px solid rgba(31, 23, 18, 0.35); background: #fff4dc;'
            }),
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Напишите, какие ощущения вызывает эта камера...',
                'style': 'width: 100%; max-width: 620px; padding: 10px; border: 1px solid rgba(31, 23, 18, 0.35); background: #fff4dc;'
            }),
            'rating': forms.Select(attrs={
                'style': 'padding: 8px; border: 1px solid rgba(31, 23, 18, 0.35); background: #fff4dc;'
            }),
        }

    def clean_author_name(self):
        author_name = self.cleaned_data.get('author_name', '').strip()

        if len(author_name) < 2:
            raise forms.ValidationError('Имя должно быть не короче 2 символов.')

        return author_name

    def clean_text(self):
        text = self.cleaned_data.get('text', '').strip()

        if len(text) < 5:
            raise forms.ValidationError('Комментарий должен быть не короче 5 символов.')

        return text