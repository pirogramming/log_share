from django.urls import path
from alarms import views

urlpatterns = [
    path('', views.Alarm.as_view(), name='alarm'),
    path('ShareMe/', views.ShareMe.as_view(), name='shareme'),
]


