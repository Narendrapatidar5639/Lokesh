from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Project

admin.site.register(Category)
admin.site.register(Project)
