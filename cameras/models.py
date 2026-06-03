from django.db import models


class CameraBrand(models.Model):
    name = models.CharField('Название бренда', max_length=100)
    country = models.CharField('Страна', max_length=100)

    class Meta:
        verbose_name = 'Бренд камеры'
        verbose_name_plural = 'Бренды камер'

    def __str__(self):
        return self.name


class Camera(models.Model):
    brand = models.ForeignKey(
        CameraBrand,
        verbose_name='Бренд',
        on_delete=models.CASCADE,
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