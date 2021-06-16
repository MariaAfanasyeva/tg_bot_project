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
    add_by_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        verbose_name="added by user_id",
        on_delete=models.SET_NULL,
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.name} by {self.author}"


class Comment(models.Model):
    to_bot = models.ForeignKey(
        Bot, related_name="bot", on_delete=models.CASCADE, verbose_name="comment to bot"
    )
    author = models.ForeignKey(
        User,
        related_name="author",
        on_delete=models.SET_NULL,
        verbose_name="comment author",
        null=True,
        blank=True,
    )
    creation_date = models.DateField(
        verbose_name="creation date", null=True, blank=True, auto_now_add=True
    )
    content = models.TextField(verbose_name="comment text")

    class Meta:
        ordering = ["creation_date"]

    def __str__(self):
        return f"comment to {self.to_bot} by {self.author}"


class Like(models.Model):
    to_bot = models.ForeignKey(
        Bot, related_name="to_bot", on_delete=models.CASCADE, verbose_name="like to bot"
    )
    author = models.ForeignKey(
        User,
        related_name="user",
        on_delete=models.SET_NULL,
        verbose_name="liked by user",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"like to {self.to_bot} by {self.author}"
