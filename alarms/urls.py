from django.urls import path
from alarms import views

app_name = 'alarms'

urlpatterns = [
    path('', views.Alarm.as_view(), name='alarm'),
    #todo 김유빈
    path('RequestGroup/', views.RequestGroup.as_view(), name='requestgroup'),
]


