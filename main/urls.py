from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.main_front, name='main_front')
]
