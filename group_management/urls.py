from django.urls import path

from group_management import views

app_name = 'group_management'

urlpatterns = [
    path('create/', views.all_create_group, name='create_group'),  # 내 그룹 리스트, 그룹생성
    path('request/to/allow/', views.allow_request, name='allow_request'),
    path('request/to/disallow/', views.disallow_request, name='disallow_request'),

    path('search/', views.search_group, name='search_group'),  # 그룹 검색 및 가입
    path('detail/<int:pk>/', views.detail_group, name='detail_group'),  # 그룹 상세 정보
    path('delete_member/', views.delete_member, name='delete_member'),  # 그룹 멤버 삭제
    path('request/<int:pk>', views.request_group, name='request_group'),  # pk group에 가입 요청하기
    path('request/withcode/', views.request_withcode, name='request_withcode'),  # 코드로 가입 요청하기

    path('delete/<int:pk>/', views.delete_group, name='delete_group'),  # 그룹 삭제
    path('secede/<int:pk>/', views.secede_group, name='secede_group'),  # 그룹 탈퇴
]
