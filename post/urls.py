from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('post_detail/<int:user_pk>/<int:post_pk>/', views.post_detail, name='post_detail'),
    path('bookmark/<int:pk>/', views.post_bookmark, name='post_bookmark'),
]