from django.db import models
from django.contrib.auth.models import User


class CameraBrand(models.Model):
    name = models.CharField('Название бренда', max_length=100)
    country = models.CharField('Страна', max_length=100)

    class Meta:
        verbose_name = 'Бренд камеры'
        verbose_name_plural = 'Бренды камер'

    def __str__(self):
        return self.name


class Camera(models.Model):
    owner = models.ForeignKey(
        User,
        verbose_name='Автор записи',
        on_delete=models.SET_NULL,
        related_name='cameras',
        null=True,
        blank=True
    )
    brand = models.ForeignKey(
        CameraBrand,
        verbose_name='Бренд',
        on_delete=models.PROTECT,
        related_name='cameras'
    )
    name = models.CharField('Название камеры', max_length=120)
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание')
    is_working = models.BooleanField('Рабочая', default=True)
    is_rare = models.BooleanField('Редкая', default=False)

    class Meta:
        verbose_name = 'Камера'
        verbose_name_plural = 'Камеры'

    def __str__(self):
        return f'{self.brand.name} {self.name}'


class CameraReview(models.Model):
    RATING_CHOICES = [
        (1, '1 — не зацепило'),
        (2, '2 — слабовато'),
        (3, '3 — нормально'),
        (4, '4 — атмосферно'),
        (5, '5 — очень вайбово'),
    ]

    camera = models.ForeignKey(
        Camera,
        verbose_name='Камера',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.SET_NULL,
        related_name='camera_reviews',
        null=True,
        blank=True
    )
    author_name = models.CharField('Имя автора', max_length=80, default='Guest')
    text = models.TextField('Комментарий')
    rating = models.IntegerField('Оценка', choices=RATING_CHOICES)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    is_visible = models.BooleanField('Показывать на сайте', default=True)

    class Meta:
        verbose_name = 'Комментарий к камере'
        verbose_name_plural = 'Комментарии к камерам'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author_name}: {self.camera.name} — {self.rating}/5'