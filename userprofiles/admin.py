from django.contrib import admin
from .models import Userprofile, Privilege

@admin.register(Userprofile)
class AdminUserprofile(admin.ModelAdmin):
    pass

@admin.register(Privilege)
class AdminPrivilege(admin.ModelAdmin):
    pass