from django.db import models
from django.contrib.auth.models import User


class Preset(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='presets'
    )
    title = models.CharField('Название пресета', max_length=120)
    tone = models.CharField('Тон', max_length=100)
    description = models.TextField('Описание')
    intensity = models.IntegerField('Интенсивность')
    is_public = models.BooleanField('Открытый', default=True)

    class Meta:
        verbose_name = 'Пресет'
        verbose_name_plural = 'Пресеты'

    def __str__(self):
        return self.title


class PresetReview(models.Model):
    RATING_CHOICES = [
        (1, '1 — не зацепило'),
        (2, '2 — слабовато'),
        (3, '3 — нормально'),
        (4, '4 — атмосферно'),
        (5, '5 — очень вайбово'),
    ]

    preset = models.ForeignKey(
        Preset,
        verbose_name='Пресет',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author_name = models.CharField('Имя автора', max_length=80)
    text = models.TextField('Комментарий')
    rating = models.IntegerField('Оценка', choices=RATING_CHOICES)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    is_visible = models.BooleanField('Показывать на сайте', default=True)

    class Meta:
        verbose_name = 'Комментарий к пресету'
        verbose_name_plural = 'Комментарии к пресетам'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author_name}: {self.preset.title} — {self.rating}/5'