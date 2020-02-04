from django.urls import path

from myprofile import views

app_name = 'myprofile'

urlpatterns = [
    path('<int:pk>/', views.profile_detail, name='profile_detail'),
    path('posting_create/', views.posting_create, name='posting_create'),
    path('posting_list', views.posting_list, name='posting_list'),
]
