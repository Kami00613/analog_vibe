from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    favorite_style = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nickname