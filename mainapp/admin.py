from django.contrib import admin

# Register your models here.
from .models import Bot, Category

admin.site.register(Bot)
admin.site.register(Category)
