from django.shortcuts import render
from .models import Preset


def preset_list(request):
    presets = Preset.objects.all()

    context = {
        'presets': presets,
    }

    return render(request, 'presets/list.html', context)