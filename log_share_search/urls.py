from django.urls import path

from log_share_search import views

urlpatterns = [
    path('search/<int:option>', views.main_search, name='main_search'),
]
