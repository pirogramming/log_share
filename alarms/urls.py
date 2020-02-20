from django.urls import path
from alarms import views

app_name = 'alarms'

urlpatterns = [
    path('', views.Alarm.as_view(), name='alarm'), #관리자가 보는 알림창
    path('detail/', views.alarm_detail, name='alarm_detail'),
    path('delete/', views.alarm_delete, name='alarm_delete'),
    path('RequestGroup/', views.RequestGroup.as_view(), name='requestgroup'), # 사용자 독촉 알림 - group_pk
]


