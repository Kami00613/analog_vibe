from django import forms

from .models import ExhibitionComment


BAD_WORDS = ['дурак', 'тупой', 'идиот']


class ExhibitionCommentForm(forms.ModelForm):
    class Meta:
        model = ExhibitionComment
        fields = ['text', 'rating']

        labels = {
            'text': 'Комментарий',
            'rating': 'Оценка',
        }

        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Напишите впечатление от этой подборки...',
                'style': 'width: 100%; max-width: 620px; padding: 10px; border: 1px solid rgba(31, 23, 18, 0.35); background: #fff4dc;'
            }),
            'rating': forms.Select(attrs={
                'style': 'padding: 8px; border: 1px solid rgba(31, 23, 18, 0.35); background: #fff4dc;'
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

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')

        if rating is not None and (rating < 1 or rating > 5):
            raise forms.ValidationError('Оценка должна быть от 1 до 5.')

        return rating