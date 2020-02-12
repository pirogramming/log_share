from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from accounts.forms import SignupModelForm, CustomUserChangeForm
from myprofile.models import BookMark, Profile

# <<<<<<<<<<<<<<profile user_pk>>>>>>>>>>>>>>
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
        profile = user.user_profile  # user -> profile

        # 최근 태그 리스트
        post_list = user.user_post.order_by('-start_date', '-end_date')  # 시작일 기준(만약 같다면 종료일 기준)으로 최근 게시물부터 태그가 들어가게 한다.
        # todo 최근 게시물의 개수제한 필요 (최근 5개 게시물이라던가)
        # 아래 딕셔너리는 orderdDict여야 하므로 파이썬 3.6 버전 이상에서만 제대로 동작하는 코드.
        recent_tags_count = {}
        for post in post_list:
            for tag in post.tags.all():
                if tag in recent_tags_count:
                    recent_tags_count[tag] += 1
                else:
                    recent_tags_count[tag] = 1

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

        context = {
            'profile': profile,
            'posts': posts,
            'recent_tags_count': recent_tags_count,
        }

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
            profile = profile_form.save()
            profile.name = request.user.last_name + request.user.first_name  # user의 이름 -> profile.name
            profile = profile.save()

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
