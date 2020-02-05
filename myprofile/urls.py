from django.urls import path

from myprofile import views

app_name = 'myprofile'

urlpatterns = [
    path('<int:pk>/', views.profile_detail, name='profile_detail'),
    path('post_create/', views.post_create, name='post_create'),
    path('post_list', views.post_list, name='post_list'),
    path('post_detail/<int:pk>', views.post_detail, name='post_detail'),
    path('post_update/<int:pk>', views.post_update, name='post_update'),
    path('post_delete/<int:pk>', views.post_delete, name='post_delete'),

]
