from django.urls import path
from .views import *

urlpatterns = [
    path('', staff, name='staff'),
    path('add/', employee_add, name='employee_add'),
    path('update/<int:pk>', employee_update, name='employee_update'),
    path('delete/<int:pk>', employee_delete, name='employee_delete'),
    path('untie/<int:pk>', untie_profile, name='untie_profile'),
    path('staffexcel/', staff_to_excel, name='staff_to_excel'),
    path('department/update/<int:pk>',
         department_update, name='department_update'),
    path('department/delete/<int:pk>',
         department_delete, name='department_delete'),
    path('department/add', department_add, name='department_add'),
]
