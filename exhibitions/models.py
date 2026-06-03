from django.db import models
from django.contrib.auth.models import User


class Exhibition(models.Model):
    curator = models.ForeignKey(
        User,
        verbose_name='Куратор',
        on_delete=models.CASCADE,
        related_name='exhibitions'
    )
    title = models.CharField('Название выставки', max_length=120)
    description = models.TextField('Описание')
    photos_count = models.IntegerField('Количество фото')
    is_published = models.BooleanField('Опубликована', default=True)

    class Meta:
        verbose_name = 'Выставка'
        verbose_name_plural = 'Выставки'

    def __str__(self):
        return self.title