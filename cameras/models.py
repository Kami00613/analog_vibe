from django.db import models


class CameraBrand(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Camera(models.Model):
    brand = models.ForeignKey(CameraBrand, on_delete=models.CASCADE, related_name='cameras')
    name = models.CharField(max_length=120)
    year = models.IntegerField()
    description = models.TextField()
    is_working = models.BooleanField(default=True)
    is_rare = models.BooleanField(default=False)

    def __str__(self):
        return self.name