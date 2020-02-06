from django.urls import path

from group_management import views

app_name = 'group_management'

urlpatterns = [
    path('create/', views.create_group, name='create_group'), # 그룹 생성
    path('update/<int:pk>/', views.update_group, name='update_group'), # 그룹 정보 변경
    path('list/', views.list_group, name='list_group'), # 그룹 리스트
    path('detail/<int:pk>/', views.detail_group, name='detail_group'), # 그룹 상세 정보
    path('request/<int:pk>/', views.request_group, name='request_group'), # 그룹 가입 요청
    path('request/from/<int:pk>/', views.request_from, name='request_from'), # pk user가 가입 요청한 리스트
    path('request/to/<int:pk>/', views.request_to, name='request_to'), # pk group으로 온 요청 리스트
]