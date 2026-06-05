from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.db import models


class Exhibition(models.Model):
    curator = models.ForeignKey(
        User,
        verbose_name='Куратор',
        on_delete=models.SET_NULL,
        related_name='exhibitions',
        null=True,
        blank=True
    )
    title = models.CharField('Название выставки', max_length=120)
    description = models.TextField('Описание')
    is_published = models.BooleanField('Опубликована', default=True)

    class Meta:
        verbose_name = 'Выставка'
        verbose_name_plural = 'Выставки'

    def __str__(self):
        return self.title

    @property
    def cover_photo(self):
        return self.photos.order_by('position', 'id').first()

    @property
    def photos_count(self):
        return self.photos.count()


class ExhibitionPhoto(models.Model):
    exhibition = models.ForeignKey(
        Exhibition,
        verbose_name='Выставка',
        on_delete=models.CASCADE,
        related_name='photos'
    )
    image_path = models.CharField(
        'Путь к картинке',
        max_length=500,
        help_text='Путь сохраняется автоматически после загрузки файла.'
    )
    caption = models.CharField(
        'Подпись',
        max_length=160,
        blank=True
    )
    position = models.PositiveIntegerField(
        'Позиция',
        default=1
    )

    class Meta:
        verbose_name = 'Фотография выставки'
        verbose_name_plural = 'Фотографии выставок'
        ordering = ['position', 'id']

    def __str__(self):
        return f'{self.exhibition.title} — фото {self.position}'

    @property
    def image_src(self):
        """
        Возвращает ссылку для <img src="...">.

        В базе хранится, например:
        exhibitions/photo_abc123.jpg

        А на сайте нужно:
        /media/exhibitions/photo_abc123.jpg
        """
        if self.image_path.startswith(('http://', 'https://', '/')):
            return self.image_path

        return default_storage.url(self.image_path)


class ExhibitionReview(models.Model):
    RATING_CHOICES = [
        (1, '1 — не зацепило'),
        (2, '2 — слабовато'),
        (3, '3 — нормально'),
        (4, '4 — атмосферно'),
        (5, '5 — очень вайбово'),
    ]

    exhibition = models.ForeignKey(
        Exhibition,
        verbose_name='Выставка',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.SET_NULL,
        related_name='exhibition_reviews',
        null=True,
        blank=True
    )
    author_name = models.CharField('Имя автора', max_length=80, default='Guest')
    text = models.TextField('Комментарий')
    rating = models.IntegerField('Оценка', choices=RATING_CHOICES)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    is_visible = models.BooleanField('Показывать на сайте', default=True)

    class Meta:
        verbose_name = 'Комментарий к выставке'
        verbose_name_plural = 'Комментарии к выставкам'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author_name}: {self.exhibition.title} — {self.rating}/5'