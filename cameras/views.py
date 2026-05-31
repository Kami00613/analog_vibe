from django.shortcuts import render
from .models import Camera


def home_page(request):
    return render(request, 'cameras/home.html')


def camera_list(request):
    cameras = Camera.objects.all()

    context = {
        'cameras': cameras,
    }

    return render(request, 'cameras/list.html', context)