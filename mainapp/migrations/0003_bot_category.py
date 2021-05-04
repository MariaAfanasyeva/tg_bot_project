# Generated by Django 3.2 on 2021-05-04 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='bot',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='mainapp.category'),
        ),
    ]