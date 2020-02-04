from django.shortcuts import render
from .models import *


# Create your views here.
def main_search(request, option):
    q = request.GET.get('q', '')  # GET request의 인자중에 q 값이 있으면 가져오고, 없으면 빈 문자열 넣기
    user = request.user
    qs = None
    # 검색창 옆에 필터 선택 -> request로 받고, 그 값에 따라 결과값 필터링 **
    if q:  # q가 있으면
        # 필터링 종류
        # option |     참조
        #   1    |  태그 & 활동내역(포스트의 제목과 내용) -> Post.(user.img + title + date?)
        #   2    |  사람명 검색
        #   3    |  그룹명 + 카테고리 필터
        if option == 1:  # 제목에 q가 포함되어 있는 레코드만 필터링 + 나랑 관련된 사람.
            qs = Post.objects.filter(title__icontains=q)
        elif option == 2:  # 이름에 q 포함 + 접속 유저와 관련된 그룹원
            qs = User.objects.filter(username__icontains=q)
        elif option == 3:  # 그룹명에 q가 포함된 그룹 + 카테고리
            qs = Custom_Group.objects.filter(name__icontains=q)

    return render(request, 'log_share_search/main_search.html', {
        'results': qs,
        'q': q,
        'option': option,
    })
