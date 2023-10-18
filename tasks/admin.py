from django.contrib import admin
from .models import Task


@admin.register(Task)
class AdminTask(admin.ModelAdmin):
    pass
