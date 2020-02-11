from django.urls import path

from search import views

app_name = 'search'

urlpatterns = [
    path('<int:option>/', views.main_search, name='main_search'),
    path('1/(?q=<tag_name>', views.tag_search, name='tag_search'),
]
