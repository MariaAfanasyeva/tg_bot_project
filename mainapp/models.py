from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='category_name')

    def __str__(self):
        return f"{self.name}"


class Bot(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    description = models.CharField(max_length=1000, verbose_name='description')
    link = models.CharField(max_length=255, verbose_name='link')
    author = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} by {self.author}"
