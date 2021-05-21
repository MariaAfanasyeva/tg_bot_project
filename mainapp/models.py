from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="category_name")

    def __str__(self):
        return f"{self.name}"


class Bot(models.Model):
    name = models.CharField(max_length=100, verbose_name="name")
    description = models.CharField(max_length=1000, verbose_name="description")
    link = models.CharField(max_length=255, verbose_name="link")
    author = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category,
        related_name="category",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.name} by {self.author}"


class Comment(models.Model):
    to_bot = models.ForeignKey(
        Bot, related_name="bot", on_delete=models.CASCADE, verbose_name="comment to bot"
    )
    author_id = models.ForeignKey(
        User,
        related_name="author",
        on_delete=models.CASCADE,
        verbose_name="comment author",
    )
    creation_date = models.DateField(
        verbose_name="creation date", null=True, blank=True, auto_now_add=True
    )
    content = models.TextField(verbose_name="comment text")

    class Meta:
        ordering = ["creation_date"]

    def __str__(self):
        return f"comment to {self.to_bot} by {self.author_id}"
