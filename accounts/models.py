from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='profile'
    )
    nickname = models.CharField('Никнейм', max_length=100, blank=True, default='')
    bio = models.TextField('Описание', blank=True)
    favorite_style = models.CharField('Любимый стиль', max_length=100, blank=True)
    phone = models.CharField('Телефон', max_length=30, blank=True, default='')

    class Meta:
        verbose_name = 'Профиль автора'
        verbose_name_plural = 'Профили авторов'

    def __str__(self):
        if self.nickname:
            return self.nickname
        return self.user.username