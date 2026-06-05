from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand

from accounts.models import Profile
from cameras.models import Camera, CameraBrand
from exhibitions.models import Exhibition, ExhibitionPhoto
from presets.models import Preset


class Command(BaseCommand):
    help = 'Заполняет базу данных демо-данными для AnalogVibe.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Начинаю заполнение базы AnalogVibe...'))

        owner = self.create_users()
        self.create_brands()
        self.create_cameras(owner)
        self.create_presets(owner)
        self.create_exhibitions(owner)

        self.stdout.write(self.style.SUCCESS('База успешно заполнена демо-данными.'))

    def copy_static_to_media(self, static_relative_path, media_relative_path):
        source_path = Path(settings.BASE_DIR) / 'static_dev' / static_relative_path

        if not source_path.exists():
            self.stdout.write(
                self.style.WARNING(f'Файл не найден: {source_path}')
            )
            return ''

        if default_storage.exists(media_relative_path):
            return media_relative_path

        with source_path.open('rb') as file:
            default_storage.save(media_relative_path, File(file))

        return media_relative_path

    def create_users(self):
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@analogvibe.local',
                'is_staff': True,
                'is_superuser': True,
            }
        )

        if created:
            admin.set_password('admin12345')
            admin.save()
        else:
            changed = False

            if not admin.is_staff:
                admin.is_staff = True
                changed = True

            if not admin.is_superuser:
                admin.is_superuser = True
                changed = True

            if changed:
                admin.save()

        owner, created = User.objects.get_or_create(
            username='Kami06666',
            defaults={
                'email': 'kami@analogvibe.local',
            }
        )

        if created:
            owner.set_password('user12345')
            owner.save()

        Profile.objects.update_or_create(
            user=owner,
            defaults={
                'nickname': 'Kami06666',
                'bio': 'Любит пленочные камеры, теплые оттенки и атмосферу старых фотоальбомов.',
                'favorite_style': 'warm grain',
                'phone': '+7 999 111-22-33',
            }
        )

        Profile.objects.update_or_create(
            user=admin,
            defaults={
                'nickname': 'Analog Admin',
                'bio': 'Администратор демо-проекта AnalogVibe.',
                'favorite_style': 'classic film',
                'phone': '',
            }
        )

        self.stdout.write(self.style.SUCCESS('Пользователи и профили созданы.'))

        return owner

    def create_brands(self):
        brands = [
            ('Canon', 'Япония'),
            ('Nikon', 'Япония'),
            ('Olympus', 'Япония'),
            ('Pentax', 'Япония'),
            ('Minolta', 'Япония'),
            ('Leica', 'Германия'),
            ('Polaroid', 'США'),
            ('Zenit', 'СССР'),
        ]

        for name, country in brands:
            CameraBrand.objects.update_or_create(
                name=name,
                defaults={
                    'country': country,
                }
            )

        self.stdout.write(self.style.SUCCESS('Бренды камер созданы.'))

    def create_cameras(self, owner):
        camera_data = [
            {
                'brand': 'Canon',
                'name': 'Canon AE-1',
                'year': 1976,
                'description': 'Классическая пленочная камера с теплым винтажным характером. Хорошо подходит для городских кадров, портретов и съемки при естественном свете.',
                'image': ('img/fill_db/cameras/canon-ae-1.jpg', 'cameras/canon-ae-1.jpg'),
                'is_working': True,
                'is_rare': False,
            },
            {
                'brand': 'Nikon',
                'name': 'Nikon FM2',
                'year': 1982,
                'description': 'Механическая пленочная камера для уличной съемки и повседневных кадров. Отличается надежным корпусом, четким управлением и атмосферой настоящей аналоговой фотографии.',
                'image': ('img/fill_db/cameras/nikon-fm2.jpg', 'cameras/nikon-fm2.jpg'),
                'is_working': True,
                'is_rare': False,
            },
            {
                'brand': 'Olympus',
                'name': 'Olympus OM-1',
                'year': 1972,
                'description': 'Компактная пленочная камера с аккуратным корпусом и мягким характером изображения. Подходит для путешествий, портретов и спокойной документальной съемки.',
                'image': ('img/fill_db/cameras/olympus-om-1.jpg', 'cameras/olympus-om-1.jpg'),
                'is_working': True,
                'is_rare': False,
            },
            {
                'brand': 'Pentax',
                'name': 'Pentax K1000',
                'year': 1976,
                'description': 'Простая и надежная камера для знакомства с пленочной фотографией. Минимум лишних элементов, понятное управление и честный механический вайб.',
                'image': ('img/fill_db/cameras/pentax-k1000.jpg', 'cameras/pentax-k1000.jpg'),
                'is_working': True,
                'is_rare': False,
            },
            {
                'brand': 'Minolta',
                'name': 'Minolta X-700',
                'year': 1981,
                'description': 'Пленочная камера с удобной автоматикой и выразительной картинкой. Хорошо подходит для портретов, прогулок по городу и теплых домашних кадров.',
                'image': ('img/fill_db/cameras/minolta-x700.jpg', 'cameras/minolta-x700.jpg'),
                'is_working': True,
                'is_rare': False,
            },
            {
                'brand': 'Leica',
                'name': 'Leica M6',
                'year': 1984,
                'description': 'Дальномерная пленочная камера с лаконичным дизайном и премиальным ощущением съемки. Подходит для репортажа, улицы и внимательной работы с композицией.',
                'image': ('img/fill_db/cameras/leica-m6.jpg', 'cameras/leica-m6.jpg'),
                'is_working': True,
                'is_rare': True,
            },
            {
                'brand': 'Polaroid',
                'name': 'Polaroid SX-70',
                'year': 1972,
                'description': 'Складная камера моментальной фотографии с узнаваемым корпусом. Создает мягкие кадры с особой винтажной атмосферой и эффектом старого фотоальбома.',
                'image': ('img/fill_db/cameras/polaroid-sx70.jpg', 'cameras/polaroid-sx70.jpg'),
                'is_working': False,
                'is_rare': True,
            },
            {
                'brand': 'Zenit',
                'name': 'Zenit-E',
                'year': 1965,
                'description': 'Советская пленочная камера с тяжелым корпусом и механическим управлением. Хорошо передает настроение старой домашней фотографии и архивных кадров.',
                'image': ('img/fill_db/cameras/zenit-e.jpg', 'cameras/zenit-e.jpg'),
                'is_working': True,
                'is_rare': False,
            },
        ]

        for data in camera_data:
            brand = CameraBrand.objects.get(name=data['brand'])
            static_path, media_path = data['image']
            image_path = self.copy_static_to_media(static_path, media_path)

            Camera.objects.update_or_create(
                name=data['name'],
                defaults={
                    'owner': owner,
                    'brand': brand,
                    'year': data['year'],
                    'description': data['description'],
                    'image_path': image_path,
                    'is_working': data['is_working'],
                    'is_rare': data['is_rare'],
                }
            )

        self.stdout.write(self.style.SUCCESS('Камеры созданы.'))

    def create_presets(self, author):
        preset_data = [
            {
                'title': 'Warm Grain',
                'tone': 'теплый',
                'intensity': 70,
                'description': 'Теплый пленочный пресет с мягкими тенями, легким зерном и уютным желтоватым оттенком. Хорошо подходит для портретов, кафе и вечерних городских кадров.',
                'image': ('img/fill_db/presets/warm-grain.jpg', 'presets/warm-grain.jpg'),
            },
            {
                'title': 'Faded Memories',
                'tone': 'выцветший',
                'intensity': 55,
                'description': 'Мягкий пресет с приглушенными цветами и эффектом старого фотоальбома. Делает кадры спокойными, немного выцветшими и архивными.',
                'image': ('img/fill_db/presets/faded-memories.jpg', 'presets/faded-memories.jpg'),
            },
            {
                'title': 'Night Film',
                'tone': 'контрастный',
                'intensity': 85,
                'description': 'Темный пленочный пресет для вечерних кадров. Усиливает тени, добавляет контраст и создает настроение ночной аналоговой съемки.',
                'image': ('img/fill_db/presets/night-film.jpg', 'presets/night-film.jpg'),
            },
            {
                'title': 'Soft Sepia',
                'tone': 'сепия',
                'intensity': 60,
                'description': 'Пресет с мягким коричневатым оттенком и спокойным контрастом. Подходит для портретов, старых зданий и атмосферных деталей.',
                'image': ('img/fill_db/presets/soft-sepia.jpg', 'presets/soft-sepia.jpg'),
            },
            {
                'title': 'Dusty Archive',
                'tone': 'архивный',
                'intensity': 75,
                'description': 'Пленочная обработка с легкой пылью, зерном и приглушенной палитрой. Хорошо выглядит на фотографиях улиц, старых комнат и предметов.',
                'image': ('img/fill_db/presets/dusty-archive.jpg', 'presets/dusty-archive.jpg'),
            },
        ]

        for data in preset_data:
            static_path, media_path = data['image']
            image_path = self.copy_static_to_media(static_path, media_path)

            Preset.objects.update_or_create(
                title=data['title'],
                defaults={
                    'author': author,
                    'tone': data['tone'],
                    'description': data['description'],
                    'intensity': data['intensity'],
                    'image_path': image_path,
                    'is_public': True,
                }
            )

        self.stdout.write(self.style.SUCCESS('Пресеты созданы.'))

    def create_exhibitions(self, curator):
        exhibition_data = [
            {
                'title': 'Пленочный город',
                'description': 'Серия городских снимков в стиле старого фотоархива: улицы, фасады, дороги, витрины и теплый свет повседневной жизни.',
                'photos': [
                    ('img/fill_db/exhibitions/film-city-1.jpg', 'exhibitions/film-city-1.jpg'),
                    ('img/fill_db/exhibitions/film-city-2.jpg', 'exhibitions/film-city-2.jpg'),
                    ('img/fill_db/exhibitions/film-city-3.jpg', 'exhibitions/film-city-3.jpg'),
                    ('img/fill_db/exhibitions/film-city-4.jpg', 'exhibitions/film-city-4.jpg'),
                ],
            },
            {
                'title': 'Тихие комнаты',
                'description': 'Атмосферная подборка интерьерных кадров с мягким светом, приглушенными цветами и ощущением старого домашнего альбома.',
                'photos': [
                    ('img/fill_db/exhibitions/quiet-rooms-1.jpg', 'exhibitions/quiet-rooms-1.jpg'),
                    ('img/fill_db/exhibitions/quiet-rooms-2.jpg', 'exhibitions/quiet-rooms-2.jpg'),
                    ('img/fill_db/exhibitions/quiet-rooms-3.jpg', 'exhibitions/quiet-rooms-3.jpg'),
                    ('img/fill_db/exhibitions/quiet-rooms-4.jpg', 'exhibitions/quiet-rooms-4.jpg'),
                ],
            },
            {
                'title': 'Шумные кадры',
                'description': 'Подборка фотографий с зерном, мягким фокусом и теплым пленочным оттенком. Главный акцент — настроение, свет и фактура кадра.',
                'photos': [
                    ('img/fill_db/exhibitions/noisy-frames-1.jpg', 'exhibitions/noisy-frames-1.jpg'),
                    ('img/fill_db/exhibitions/noisy-frames-2.jpg', 'exhibitions/noisy-frames-2.jpg'),
                    ('img/fill_db/exhibitions/noisy-frames-3.jpg', 'exhibitions/noisy-frames-3.jpg'),
                    ('img/fill_db/exhibitions/noisy-frames-4.jpg', 'exhibitions/noisy-frames-4.jpg'),
                ],
            },
            {
                'title': 'Ночной архив',
                'description': 'Темные городские фотографии с огнями, отражениями и контрастными тенями. Подборка передает атмосферу поздних прогулок и пленочной ночной съемки.',
                'photos': [
                    ('img/fill_db/exhibitions/night-archive-1.jpg', 'exhibitions/night-archive-1.jpg'),
                    ('img/fill_db/exhibitions/night-archive-2.jpg', 'exhibitions/night-archive-2.jpg'),
                    ('img/fill_db/exhibitions/night-archive-3.jpg', 'exhibitions/night-archive-3.jpg'),
                    ('img/fill_db/exhibitions/night-archive-4.jpg', 'exhibitions/night-archive-4.jpg'),
                ],
            },
        ]

        for data in exhibition_data:
            exhibition, created = Exhibition.objects.update_or_create(
                title=data['title'],
                defaults={
                    'curator': curator,
                    'description': data['description'],
                    'is_published': True,
                }
            )

            exhibition.photos.all().delete()

            for position, photo_data in enumerate(data['photos'], start=1):
                static_path, media_path = photo_data
                image_path = self.copy_static_to_media(static_path, media_path)

                if not image_path:
                    continue

                ExhibitionPhoto.objects.create(
                    exhibition=exhibition,
                    image_path=image_path,
                    caption=f'Фото {position}',
                    position=position
                )

        self.stdout.write(self.style.SUCCESS('Выставки и фотографии созданы.'))