from django.urls import path
from .views import index, get_tasks_count, chatgpt

urlpatterns = [
    path('', index, name='home'),
    path('api/counttasks', get_tasks_count, name='get_tasks_count'),
    path('chatgpt/', chatgpt, name='chatgpt'),
]
