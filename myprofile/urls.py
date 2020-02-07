from django.urls import path
from . import views

app_name = 'myprofile'

urlpatterns = [
    path('<int:pk>/', views.profile_detail, name='profile_detail'),
    path('bookmark_list/<int:pk>/', views.bookmark_list, name='bookmark_list'),
    path('bookmark_delete/<int:pk>/', views.bookmark_delete, name='bookmark_delete'),
]