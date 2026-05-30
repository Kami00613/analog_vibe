from django.shortcuts import render


MOCK_EXHIBITIONS = [
    {
        'title': 'Шумные кадры',
        'description': 'Подборка фотографий с зерном, мягким фокусом и теплым светом.',
        'photos_count': 18,
    },
    {
        'title': 'Пленочный город',
        'description': 'Серия городских снимков в стиле старого фотоархива.',
        'photos_count': 24,
    },
    {
        'title': 'Тихие комнаты',
        'description': 'Атмосферные интерьерные кадры с приглушенными цветами и мягкими тенями.',
        'photos_count': 12,
    },
]


def exhibition_list(request):
    context = {
        'exhibitions': MOCK_EXHIBITIONS,
    }

    return render(request, 'exhibitions/list.html', context)