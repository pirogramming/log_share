from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
