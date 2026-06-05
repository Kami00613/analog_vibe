from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST

from .forms import CustomRegisterForm, ProfileForm
from .models import Profile


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('cameras:home')


def serialize_form_errors(form):
    errors = {}

    for field_name, field_errors in form.errors.items():
        errors[field_name] = [str(error) for error in field_errors]

    return errors


def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            Profile.objects.get_or_create(
                user=user,
                defaults={
                    'nickname': user.username,
                }
            )

            login(request, user)

            return redirect('cameras:home')
    else:
        form = CustomRegisterForm()

    context = {
        'form': form,
    }

    return render(request, 'accounts/register.html', context)


@require_POST
def check_password_reset_email(request):
    """
    AJAX-проверка email перед сбросом пароля.

    Если пользователь ввел email, которого нет в базе,
    страница не перезагружается — JS просто показывает ошибку под полем.
    """
    email = request.POST.get('email', '').strip()

    if not email:
        return JsonResponse({
            'exists': False,
            'message': 'Введите email.'
        }, status=400)

    user_exists = User.objects.filter(
        email__iexact=email,
        is_active=True
    ).exists()

    if not user_exists:
        return JsonResponse({
            'exists': False,
            'message': 'Пользователь с такой почтой не найден.'
        }, status=404)

    return JsonResponse({
        'exists': True,
        'message': ''
    })


@login_required
def profile_page(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            'nickname': request.user.username,
        }
    )

    context = {
        'profile': profile,
    }

    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            'nickname': request.user.username,
        }
    )

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()

            if is_ajax:
                return JsonResponse({
                    'success': True,
                    'redirect_url': reverse('accounts:profile'),
                })

            return redirect('accounts:profile')

        if is_ajax:
            return JsonResponse({
                'success': False,
                'errors': serialize_form_errors(form),
            }, status=400)
    else:
        form = ProfileForm(instance=profile)

    context = {
        'profile': profile,
        'form': form,
    }

    return render(request, 'accounts/profile_edit.html', context)