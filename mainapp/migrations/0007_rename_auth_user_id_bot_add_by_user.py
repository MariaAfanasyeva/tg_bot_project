# Generated by Django 3.2 on 2021-05-28 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0006_alter_bot_auth_user_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="bot",
            old_name="auth_user_id",
            new_name="add_by_user",
        ),
    ]
