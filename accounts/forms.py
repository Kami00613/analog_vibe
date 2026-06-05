from django import forms
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Введите email',
            'style': 'width: 100%; padding: 10px; border: 1px solid rgba(31, 23, 18, 0.35); background: #fff4dc;'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Логин',
            'email': 'Email',
            'password1': 'Пароль',
            'password2': 'Повторите пароль',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Например: Lena066',
                'style': 'width: 100%; padding: 10px; border: 1px solid rgba(31, 23, 18, 0.35); background: #fff4dc;'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Придумайте пароль',
            'style': 'width: 100%; padding: 10px; border: 1px solid rgba(31, 23, 18, 0.35); background: #fff4dc;'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Повторите пароль',
            'style': 'width: 100%; padding: 10px; border: 1px solid rgba(31, 23, 18, 0.35); background: #fff4dc;'
        })

        for field in self.fields.values():
            field.help_text = ''

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует.')

        return email


class ExistingUserPasswordResetForm(PasswordResetForm):
    """
    Форма для сброса пароля.

    Стандартная PasswordResetForm из Django специально не говорит,
    существует пользователь или нет. Для учебного задания делаем явную
    проверку, чтобы при несуществующей почте пользователь оставался
    на этой же странице и видел понятную ошибку.
    """

    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Введите email',
            'autocomplete': 'email',
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()

        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError('Пользователь с такой почтой не найден.')

        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'bio', 'favorite_style', 'phone']

        labels = {
            'nickname': 'Никнейм',
            'bio': 'О себе',
            'favorite_style': 'Любимый стиль',
            'phone': 'Телефон',
        }

        widgets = {
            'nickname': forms.TextInput(attrs={
                'placeholder': 'Например: Lena',
                'style': 'width: 100%; padding: 10px; border: 1px solid rgba(31, 23, 18, 0.35); background: #fff4dc;'
            }),
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Расскажите немного о себе и своем визуальном вкусе...',
                'style': 'width: 100%; padding: 10px; border: 1px solid rgba(31, 23, 18, 0.35); background: #fff4dc;'
            }),
            'favorite_style': forms.TextInput(attrs={
                'placeholder': 'Например: warm grain, street archive, soft fade',
                'style': 'width: 100%; padding: 10px; border: 1px solid rgba(31, 23, 18, 0.35); background: #fff4dc;'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Например: +7 999 123-45-67',
                'style': 'width: 100%; padding: 10px; border: 1px solid rgba(31, 23, 18, 0.35); background: #fff4dc;'
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()

        if not phone:
            return phone

        clean_p = (
            phone
            .replace(' ', '')
            .replace('-', '')
            .replace('(', '')
            .replace(')', '')
        )

        if not clean_p.replace('+', '').isdigit():
            raise forms.ValidationError('Телефон должен содержать только цифры, пробелы, скобки, дефисы и плюс.')

        if not (clean_p.startswith('+7') or clean_p.startswith('8')):
            raise forms.ValidationError('Телефон должен начинаться с +7 или 8.')

        return phone