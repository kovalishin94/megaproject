from django.urls import path
from .views import *

urlpatterns = [
    path('', tests, name='tests'),
    path('<int:pk>', edit_test, name='edit_test'),
    path('delete/<int:pk>', delete_test, name='delete_test'),
    path('update/<int:pk>', update_test, name='update_test'),
    path('deletequestion/<int:pk>', delete_question, name='delete_question'),
    path('updatequestion/<int:pk>', update_question, name='update_question'),
    path('addchoice/<int:pk>', add_choice, name='add_choice'),
    path('deletechoice/<int:pk>', delete_choice, name='delete_choice'),
    path('solvetest/<int:pk>', solve_test, name='solve_test'),
    path('resulttest/<int:pk>', result_test, name='result_test'),
    path('allresults/<int:pk>', all_test_results, name='all_test_results'),
]
