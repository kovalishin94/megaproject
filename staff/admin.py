from django.contrib import admin
from .models import Employee, Department


@admin.register(Employee)
class AdminEmployee(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ('id', 'last_name', 'first_name', 'surname', 'date_of_birth',
                    'email', 'department', 'agreement_date', 'created_at')
    list_display_links = ('last_name',)


@admin.register(Department)
class AdminDepartment(admin.ModelAdmin):
    pass
