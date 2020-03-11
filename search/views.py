from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from taggit.models import Tag

from group_management.models import CustomGroup, GroupRequest
from post.models import Post
from .models import *

# Create your views here.
from .utils import *


def main_search(request):
    q = request.GET.get('q', '')  # GET request의 인자중에 q 값이 있으면 가져오고, 없으면 빈 문자열 넣기
    option = request.GET.get('options', '')
    # category = request.GET.get()
    user = request.user
    print('Request:', request.GET.keys())
    qs = None
    # 검색창 옆에 필터 선택 -> request로 받고, 그 값에 따라 결과값 필터링 **
    if q:  # q가 있으면

        if option == 'posts':  # 제목에 q가 포함되어 있는 레코드만 필터링 + 나랑 관련된 사람.
            qs = filter_posts(q, user)
            print('option: posts')
        elif option == 'tags':  # 이름에 q 포함 + 접속 유저와 관련된 그룹원
            qs = filter_tags(q, user)
            print('option: tags')

        elif option == 'users':  # 그룹명에 q가 포함된 그룹
            qs = filter_users(q, user)
            print('option: users')

    else:
        qs = Post.objects.filter(user__user_groups__in=user.user_groups.all()).distinct()

    groupid = set(user.user_groups.values_list('id', flat=True))
    try:
        selected_groupid = set(map(int, group_id_list(request, user)))
    except TypeError:
        selected_groupid = groupid

    unselected_groupid = groupid - selected_groupid
    print("카테고리 필터링 전", qs)
    qs = process_category(request, user, qs)

    print("카테고리 필터링 후: ", qs)
    bm_list = user.user_bookmark.values_list('post_id', flat=True)
    print('북마크 리스트', bm_list)
    print('그룹 체크박스', list(selected_groupid))
    print('그룹', unselected_groupid)
    posts = None
    if qs:

        paginator = Paginator(qs, 3)
        page = request.POST.get('page')

        try:
            posts = paginator.page(page)  # 해당 페이지의 포스트(post_list)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

    # print(paginator, page)
    # print(posts)
    # print('Request.GET:', request.GET)
    # print(qs)

    manage_groups = list(request.user.user_manage_groups.all())
    request_messages = list()
    for g in manage_groups:
        request_messages += list(GroupRequest.objects.filter(group=g))
    return render(request, 'search/main.html', {
        'request': request,
        # 'results': qs,   # 1: post, 2: user
        'results': qs,
        'q': q,
        'groups': user.user_groups.all(),
        'posts': posts,
        'option': option,
        'request_messages_cnt': len(request_messages),
        'bm_post_list': bm_list,
        'selected_groupid': list(unselected_groupid),
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
    q = tag_name
    qs = filter_tags(q, user)
    print(qs)
    results = {'posts': qs}
    return render(request, 'search/main.html', {
        'request': request,
        'posts': qs,
        'q': q,
        'option': 'posts',
    })


def search_auto(request):
    user = request.user
    q = request.GET.get('q', '')
    option = request.GET['option']
    results = None
    print('Ajax요청', q, option)
    if option == 'posts':
        qs = filter_posts(q, user)
        results = [
            {
                'id': post.id,
                'name': post.title,
            } for post in qs
        ]
    elif option == 'tags':
        # qs = Post.tags.filter(post__user__user_groups__in=user.user_groups.all())
        qs = Tag.objects.filter(
            Q(post__user__user_groups__in=user.user_groups.all()) &
            Q(name__icontains=q)
        ).distinct()
        results = [
            {
                'id': tag.id,
                'name': tag.name,
            } for tag in qs
        ]
    elif option == 'users':
        # qs = User.objects.filter(user_groups__in=user.user_groups.all()).distinct()
        print(User.objects.filter(user_groups__in=user.user_groups.all()))
        qs = User.objects.filter(
            Q(user_groups__in=user.user_groups.all()) &
            (Q(user_profile__name__icontains=q) | Q(username__icontains=q))
        ).distinct()
        results = [
            {
                'id': users.id,
                'name': users.user_profile.name
            } for users in qs
        ]

    print('Ajax응답', results)

    data = {
        'results': results,
    }
    return JsonResponse(
        data,
        json_dumps_params={'ensure_ascii': False}
    )


def search_scroll(request):
    q = request.GET.get('q', '')  # GET request의 인자중에 q 값이 있으면 가져오고, 없으면 빈 문자열 넣기
    option = request.GET.get('options', '')
    user = request.user
    qs = None
    print('스크롤 GET요청', request.GET.values())
    if q:  # q가 있으면

        if option == 'posts':  # 제목에 q가 포함되어 있는 레코드만 필터링 + 나랑 관련된 사람.
            qs = filter_posts(q, user)
            print('option: posts')
        elif option == 'tags':  # 이름에 q 포함 + 접속 유저와 관련된 그룹원
            qs = filter_tags(q, user)
            print('option: tags')

        elif option == 'users':  # 그룹명에 q가 포함된 그룹
            qs = filter_users(q, user)
            print('option: users')

    else:
        qs = Post.objects.filter(user__user_groups__in=user.user_groups.all()).distinct()

    qs = process_category(request, user, qs)
    post_list = qs
    paginator = Paginator(post_list, 3)
    page = request.GET.get('page')  # ajax로부터 POST 타입을 전달받음
    bm_list = user.user_bookmark.values_list('post_id', flat=True)

    try:
        posts = paginator.page(page)  # 해당 페이지의 포스트(post_list)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    print(page, posts)
    print('--')
    context = {
        'posts': posts,
        'bm_post_list': bm_list,

    }
    return render(request, 'search/main_search.html', context)  # ajax_datatype => dataType: 'html'
