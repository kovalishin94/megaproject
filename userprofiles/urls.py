from django.urls import path
from .views import *

urlpatterns = [
    path('auth/', authentication, name='auth'),
    path('logout/', logout_view, name='logout'),
    path('', users, name='users'),
    path('create/', user_create, name='user_create'),
    path('update/<int:pk>', user_update, name='user_update'),
    path('delete/<int:pk>', user_delete, name='user_delete'),
]
