from django.db import models


class Bot(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    description = models.CharField(max_length=1000, verbose_name='description')
    link = models.CharField(max_length=255, verbose_name='link')
    author = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} by {self.author}"
