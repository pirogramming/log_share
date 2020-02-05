from django.urls import path

from group_management import views

app_name = 'group_management'

urlpatterns = [
    path('create/', views.create_group, name='create_group'),
    path('update/<int:pk>/', views.update_group, name='update_group'),
    path('list/', views.list_group, name='list_group'),
    path('detail/<int:pk>/', views.detail_group, name='detail_group'),
    path('request/<int:pk>/', views.request_group, name='request_group'),
    path('request/from/<int:pk>/', views.request_from, name='request_from'),
    path('request/to/<int:pk>/', views.request_to, name='request_to'),
]