from django.urls import path
from . import views

app_name = 'myprofile'

urlpatterns = [
    path('<int:pk>/', views.profile_detail, name='profile_detail'),
    path('bookmark_list/<int:pk>/', views.bookmark_list, name='bookmark_list'),
    #path('post_detail/<int:user_pk>/<int:post_pk>/', views.post_detail, name='post_detail'),
]