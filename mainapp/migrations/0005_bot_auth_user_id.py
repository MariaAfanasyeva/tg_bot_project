# Generated by Django 3.2 on 2021-05-20 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0004_alter_bot_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="bot",
            name="auth_user_id",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="added by user_id"
            ),
        ),
    ]
