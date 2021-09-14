from django.contrib import admin
from .models import Task # import Task model // models.py

admin.site.register(Task) # register Task model to admin panel
