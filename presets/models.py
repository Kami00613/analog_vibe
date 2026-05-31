from django.db import models
from django.contrib.auth.models import User


class Preset(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='presets')
    title = models.CharField(max_length=120)
    tone = models.CharField(max_length=100)
    description = models.TextField()
    intensity = models.IntegerField()
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.title