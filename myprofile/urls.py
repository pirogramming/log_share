from django.urls import path
from . import views

app_name = 'myprofile'

urlpatterns = [
    path('profile/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('bookmark_list/<int:pk>/', views.bookmark_list, name='bookmark_list'),
    path('post_detail/<int:pk1>/<int:pk2>/', views.post_detail, name='post_detail'),
]