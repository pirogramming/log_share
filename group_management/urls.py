from django.contrib import admin
from django.urls import path, include

from group_management import views

app_name = 'group_management'

urlpatterns = [
    path('create/', views.create_group, name='create_group'),
    path('update/<int:pk>/', views.update_group, name='update_group'),
    path('list/', views.list_group, name='list_group'),
    path('detail/<int:pk>/', views.detail_group, name='detail_group'),
    path('request/<int:pk>/', views.request_group, name='request_group'),
    path('request/list/<int:pk>/', views.request_list, name='request_list'),
]