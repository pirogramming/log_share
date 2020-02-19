from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from accounts.forms import SignupModelForm, CustomUserChangeForm
from myprofile.models import BookMark, Profile
from random import randint

# <<<<<<<<<<<<<<profile user_pk>>>>>>>>>>>>>>
from myprofile.utils import recent_tag_counting
from post.models import Post


@login_required
def profile_detail(request, pk):
    # 본인 or 관련 그룹원
    try:
        ans = False
        user = User.objects.get(pk=pk)  # 프로필의 user
        # 들어가려는 프로필이 본인의 프로필이 아니면서(타인의 프로필이면서) 프로필 user가 request.user의 그룹에 포함되지 않다면
        if request.user.id != user.pk:
            for group in request.user.user_groups.all():
                if user in group.members.all():
                    ans = True
                    break

            if ans == False:
                raise NotImplementedError

    except NotImplementedError:
        return render(request, 'http404.html')

    else:
        try:
            profile = user.user_profile  # user -> profile
        except Exception:
            if user == request.user:
                return redirect('accounts:signup_profile')
            else:
                return render(request, 'http404.html')

        # 최근 태그 리스트
        post_list = user.user_post.order_by('-start_date', '-end_date')# 시작일 기준(만약 같다면 종료일 기준)으로 최근 게시물부터 태그가 들어가게 한다.
        # 최상단 10개 개시물에서 태그들이 얼마나 많이 사용되었는지 카운팅하는 함수
        recent_tags_count=recent_tag_counting(post_list)

        # myprofile:profile_detail과 post:myprofile_post_list가 연동된 상태
        # myprofile:profile_detail 내 post:myprofile_post_list가 처음 화면
        # 스크롤을 내리면 post:myprofile_post_list_ajax 실행
        paginator = Paginator(post_list, 2)  # 한페이지에 담길 포스트 갯수
        page = request.GET.get('page')  # 첫 화면의 페이지(GET)



        try:
            posts = paginator.page(page)  # page(): 몇번째 페이지 리턴
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)  # num_pages : 총 페이지 수

        colors = ('red', 'green', 'blue', 'yellow', 'brown')
        context = {
            'profile': profile,
            'posts': posts,
            'recent_tags_count': recent_tags_count,
            'colors': colors,
        }
        if profile.interested_tag:
            interested_tag_list = profile.interested_tag.split(',')
            interested_tag_dict = {tag: randint(1, 3) for tag in interested_tag_list}

            context['interested_tag_dict'] = interested_tag_dict

        return render(request, 'myprofile/profile_detail.html', context)


@login_required
def profile_edit(request, pk):
    user = User.objects.get(pk=pk)
    profile = user.user_profile

    if request.method == "POST":
        user_change_form = CustomUserChangeForm(
            request.POST,
            instance=user
        )
        profile_form = SignupModelForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_change_form.is_valid() and profile_form.is_valid():
            user_change_form.save()
            profile = profile_form.save(commit=False)
            profile.name = request.user.last_name + request.user.first_name  # user의 이름 -> profile.name
            profile.save()

            return redirect('myprofile:profile_detail', request.user.pk)

    elif request.method == "GET":
        user_change_form = CustomUserChangeForm(instance=user)
        profile_form = SignupModelForm(instance=profile)

    return render(request, 'myprofile/profile_edit.html', {
        'user_change_form': user_change_form,
        'profile_form': profile_form,
    })


# user_pk / 해당 user의 bookmark_list
def bookmark_list(request, pk):
    user = User.objects.get(pk=pk)
    bookmarks = user.user_bookmark.all()

    context = {
        'bookmarks': bookmarks,
    }

    return render(request, 'myprofile/bookmark_list.html', context)


# pk : bookmark.pk
def bookmark_delete(request, pk):
    bookmark = BookMark.objects.get(pk=pk)
    bookmark.delete()

    return redirect('myprofile:bookmark_list', bookmark.user.pk)
