from django.db import models
from django.contrib.auth.models import User


class Exhibition(models.Model):
    curator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exhibitions')
    title = models.CharField(max_length=120)
    description = models.TextField()
    photos_count = models.IntegerField()
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title