from django.urls import path

from group_management import views

app_name = 'group_management'

urlpatterns = [
    path('create/', views.create_group, name='create_group'), # 그룹 생성
    path('manage/list/',  views.manage_list, name='mangage_list'), # 내가 관리자인 그룹 리스트
    path('update/<int:pk>/', views.update_group, name='update_group'), # 그룹 정보 변경
    path('request/to/', views.request_to, name='request_to'), # 현재유저가 그룹장인 그룹으로 온 요청 리스트
    path('request/to/allow/', views.allow_request, name='allow_request'),
    path('request/to/disallow/', views.disallow_request, name='disallow_request'),

    path('all/', views.all_group, name='all_group'), # 내가 가입한 그룹 리스트
    path('detail/<int:pk>/', views.detail_group, name='detail_group'), # 그룹 상세 정보
    #추가
    path('delete_member/', views.delete_member, name='delete_member'), # 그룹 멤버
    #추가끝
    path('request/<int:pk>', views.request_group, name='request_group'), # pk group에 가입 요청하기
    path('request/withcode/', views.request_withcode, name='request_withcode'), # 코드로 가입 요청하기
    path('request/from/<int:pk>/', views.request_from, name='request_from'), # pk user가 가입 요청한 리스트

    path('delete/<int:pk>/', views.delete_group, name='delete_group'),
    path('secede/<int:pk>/', views.secede_group, name='secede_group'),
]
