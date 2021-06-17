from django.contrib import admin

# Register your models here.
from .models import Bot, Category, Comment, Like

admin.site.register(Bot)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Like)
