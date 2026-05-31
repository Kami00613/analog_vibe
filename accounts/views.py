from django.shortcuts import render
from .models import Profile


def profile_page(request):
    profile = Profile.objects.first()

    context = {
        'profile': profile,
    }

    return render(request, 'accounts/profile.html', context)