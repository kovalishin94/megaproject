from django.urls import path
from .views import index, get_tasks_count, chatgpt, EmployeeOverdueTask

urlpatterns = [
    path('', index, name='home'),
    path('api/counttasks', get_tasks_count, name='get_tasks_count'),
    path('api/v1/top3overdue/', EmployeeOverdueTask.as_view({'get': 'list'})),
    path('chatgpt/', chatgpt, name='chatgpt'),

]
