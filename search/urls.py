from django.urls import path

from search import views

app_name = 'search'

urlpatterns = [
    # path('<int:option>/', views.main_search, name='main_search'),
    # path('?q=<tag_name>/', views.tag_search, name='tag_search'),
    path('ajax/', views.search_auto, name='search_auto'),
    path('ajax/scroll/', views.search_scroll, name='search_scroll'),
    path('', views.main_search, name='main_search'),
]
