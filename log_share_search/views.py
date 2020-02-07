from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect

from group_management.models import CustomGroup
from post.models import Post
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
        # user.groups.all() with reqeust.user.
        if option == 1:  # 제목에 q가 포함되어 있는 레코드만 필터링 + 나랑 관련된 사람.
            # 필터링 종류 #
            # 그룹 필터링
            # 기간 필터링(시간, 최신순)
            # 포스트 카테고리

            qs = Post.objects.filter(
                Q(user__groups__in=user.groups.all()) & # 나와 관련된 유저들
                (Q(title__icontains=q) | Q(tags__name__icontains=q) | Q(contents__icontains=q))
            ).distinct() # 중복 제거
            # qs = relate_post.objects.filter(
            #     # 포스트 내용 필요한가? 내용 미리보기 필요할듯..(해당 키워드가 담긴 문장을 보여준다던지..)
            #     Q(title__icontains=q) | Q(tag__word__icontains=q) | Q(contents__icontains=q)
            # ).distinct()
        elif option == 2:  # 이름에 q 포함 + 접속 유저와 관련된 그룹원
            # 필터링 종류 #
            # 그룹 필터링
            qs = User.objects.filter(
                Q(groups__in=user.groups.all()) &
                (Q(user_profile__name__icontains=q) | Q(username__icontains=q))
            )
        elif option == 3:  # 그룹명에 q가 포함된 그룹
            # 필터링 종류 #
            # 그룹 카테고리
            # if request.user.groups in filtered_group: 해당 그룹원의 최신 포스팅도 같이?
            qs = CustomGroup.objects.filter(
                Q(name__icontains=q) & Q(is_searchable=True)
            )



    return render(request, 'log_share_search/main_search.html', {
        'request': request,
        'results': qs,
        'q': q,
        'option': option,
    })

def tag_search(request, tag_name):
    '''
    :param tag_name:
    specific tag_name at post_detail or post_list,
    to search related posts directly.
    :return:
    main_search(option 1 -title, contents, tag-) post list
    '''
    user = request.user
    q=tag_name

    qs = None
    qs = Post.objects.filter(
        Q(user__groups__in=user.groups.all()) &
        Q(tags__name__icontains=q)
    ).distinct()  # 중복 제거

    return render(request, 'log_share_search/main_search.html', {
        'request': request,
        'results': qs,
        'q': q,
        'option': 1,
    })





# 피드 - 최근 포스팅
# 그룹 -

