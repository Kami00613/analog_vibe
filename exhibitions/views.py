from django.shortcuts import render
from .models import Exhibition


def exhibition_list(request):
    exhibitions = Exhibition.objects.all()

    context = {
        'exhibitions': exhibitions,
    }

    return render(request, 'exhibitions/list.html', context)