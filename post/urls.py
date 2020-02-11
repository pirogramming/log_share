from django.urls import path
from post import views

app_name = 'post'

urlpatterns = [
    # path('', views.post_list, name='post_list'),
    path('post_create/', views.post_create, name='post_create'),
    path('post_detail/<int:pk>/', views.post_detail, name='post_detail'),
    path('post_update/<int:pk>/', views.post_update, name='post_update'),
    path('post_delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('search/', views.Search.as_view(), name='post_search'),
    path('bookmark/', views.post_bookmark, name='post_bookmark'),
    path('post_scroll_list/<int:pk>/', views.post_scroll_list, name='post_scroll_list')
]
