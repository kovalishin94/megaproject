from django.urls import path
from tasks.views import *

urlpatterns = [
    path('', tasks, name='tasks'),
    path('solved/', solvedtasks, name='solvedtasks'),
    path('newtasks/', newtasks, name='newtasks'),
    path('delegatedtasks/', delegatedtasks, name='delegatedtasks'),
    path('acceptedtasks/', acceptedtasks, name='acceptedtasks'),
    path('add/', task_add, name='task_add'),
    path('delete/<int:pk>', task_delete, name='task_delete'),
    path('update/<int:pk>', task_update, name='task_update'),
    path('accept/<int:pk>', task_accept, name='task_accept'),
    path('answer/<int:pk>', task_answer, name='task_answer'),
    path('solve/<int:pk>', task_solve, name='task_solve'),
    path('receive/<int:pk>', task_to_receive, name='task_to_receive'),
]
