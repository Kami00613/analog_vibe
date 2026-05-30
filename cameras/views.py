from django.shortcuts import render


MOCK_CAMERAS = [
    {
        'name': 'Zenit-E',
        'brand': 'Зенит',
        'year': 1965,
        'description': 'Пленочная камера с механическим управлением. Подходит для спокойной съемки и теплых кадров.',
        'is_working': True,
        'is_rare': False,
    },
    {
        'name': 'Canon AE-1',
        'brand': 'Canon',
        'year': 1976,
        'description': 'Японская камера, которую часто выбирают для знакомства с пленочной фотографией.',
        'is_working': True,
        'is_rare': True,
    },
    {
        'name': 'Polaroid SX-70',
        'brand': 'Polaroid',
        'year': 1972,
        'description': 'Камера для моментальных снимков с узнаваемым складным корпусом.',
        'is_working': False,
        'is_rare': True,
    },
    {
        'name': 'FED-5',
        'brand': 'ФЭД',
        'year': 1977,
        'description': 'Дальномерная камера для тех, кто любит ручные настройки и старую оптику.',
        'is_working': True,
        'is_rare': False,
    },
]


def home_page(request):
    return render(request, 'cameras/home.html')


def camera_list(request):
    context = {
        'cameras': MOCK_CAMERAS,
    }

    return render(request, 'cameras/list.html', context)