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