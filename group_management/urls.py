from django.urls import path

from group_management import views

app_name = 'group_management'

urlpatterns = [
    path('create/', views.all_create_group, name='create_group'), # 그룹 생성제
    path('update/<int:pk>/', views.update_group, name='update_group'), # 그룹 정보 변경
    path('request/to/allow/', views.allow_request, name='allow_request'),
    path('request/to/disallow/', views.disallow_request, name='disallow_request'),

    path('search/', views.search_group, name='search_group'), # 그룹 검색 및 가입
    # path('all/', views.all_group, name='all_group'), # 내가 가입한 그룹 리스트
    path('detail/<int:pk>/', views.detail_group, name='detail_group'), # 그룹 상세 정보
    path('delete_member/', views.delete_member, name='delete_member'), # 그룹 멤버 삭제
    path('request/<int:pk>', views.request_group, name='request_group'), # pk group에 가입 요청하기
    path('request/withcode/', views.request_withcode, name='request_withcode'), # 코드로 가입 요청하기
    path('request/from/', views.request_from, name='request_from'), # 접속한 user가 가입 요청한 리스트

    path('delete/<int:pk>/', views.delete_group, name='delete_group'),
    path('secede/<int:pk>/', views.secede_group, name='secede_group'),
]
