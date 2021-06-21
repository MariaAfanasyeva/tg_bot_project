import inspect

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver


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


class Audit(models.Model):
    create_time = models.DateTimeField(
        verbose_name="create time", auto_now_add=True, null=True, blank=True
    )
    table_name = models.CharField(
        max_length=50, verbose_name="table", null=True, blank=True
    )
    field_name = models.CharField(
        max_length=75, verbose_name="field", null=True, blank=True
    )
    old_value = models.TextField(verbose_name="old value", null=True, blank=True)
    new_value = models.TextField(verbose_name="new value", null=True, blank=True)
    author_id = models.IntegerField(verbose_name="author", null=True, blank=True)
    record_id = models.IntegerField(verbose_name="record id", null=True, blank=True)

    def __str__(self):
        return f"Author with id {self.author_id} changed table {self.table_name} at {self.create_time}"


@receiver(pre_save, sender=Category)
@receiver(pre_save, sender=Bot)
@receiver(pre_save, sender=Comment)
@receiver(pre_save, sender=Like)
def pre_save_signal_handler(sender, instance, **kwargs):
    for frame_record in inspect.stack():
        if frame_record[3] == "get_response":
            request = frame_record[0].f_locals["request"]
            user = request.user
            break
    else:
        request = None
        user = None
    model_fields = []
    for field in instance._meta.fields:
        model_fields.append(field.name)
    new_obj = instance
    model_name = sender.__name__
    if instance.id:
        old_obj = sender.objects.get(id=instance.id)
        for field in model_fields:
            if getattr(old_obj, field) != getattr(new_obj, field):
                old_val = sender._meta.get_field(field).value_from_object(old_obj)
                new_val = sender._meta.get_field(field).value_from_object(new_obj)
                Audit.objects.create(
                    table_name=model_name,
                    field_name=field,
                    old_value=old_val,
                    new_value=new_val,
                    author_id=user.id,
                    record_id=instance.id,
                )
    else:
        for field in model_fields:
            new_val = sender._meta.get_field(field).value_from_object(new_obj)
            Audit.objects.create(
                table_name=model_name,
                field_name=field,
                old_value=None,
                new_value=new_val,
                author_id=user.id,
                record_id=None,
            )


@receiver(pre_delete, sender=Category)
@receiver(pre_delete, sender=Bot)
@receiver(pre_delete, sender=Comment)
@receiver(pre_delete, sender=Like)
def pre_delete_signal_handler(sender, instance, **kwargs):
    for frame_record in inspect.stack():
        if frame_record[3] == "get_response":
            request = frame_record[0].f_locals["request"]
            user = request.user
            break
    else:
        request = None
        user = None
    model_fields = []
    for field in instance._meta.fields:
        model_fields.append(field.name)
    model_name = sender.__name__
    old_obj = sender.objects.get(id=instance.id)
    for field in model_fields:
        old_val = sender._meta.get_field(field).value_from_object(old_obj)
        Audit.objects.create(
            table_name=model_name,
            field_name=field,
            old_value=old_val,
            new_value=None,
            author_id=user.id,
            record_id=instance.id,
        )
