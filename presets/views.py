from django.shortcuts import render


MOCK_PRESETS = [
    {
        'title': 'Warm Grain',
        'tone': 'теплый',
        'description': 'Мягкий теплый пресет с зерном, желтоватыми оттенками и эффектом старой пленки.',
        'intensity': 70,
        'is_public': True,
    },
    {
        'title': 'Faded Memories',
        'tone': 'выцветший',
        'description': 'Пресет с бледными цветами, мягким контрастом и ощущением старого фотоальбома.',
        'intensity': 55,
        'is_public': True,
    },
    {
        'title': 'Night Film',
        'tone': 'контрастный',
        'description': 'Темный пресет для вечерних кадров с глубокими тенями и холодными бликами.',
        'intensity': 85,
        'is_public': False,
    },
]


def preset_list(request):
    context = {
        'presets': MOCK_PRESETS,
    }

    return render(request, 'presets/list.html', context)