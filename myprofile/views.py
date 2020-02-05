from django.shortcuts import render
from .models import Profile, BookMark
from django.contrib.auth.models import User


def profile_detail(request, pk):
    user = User.objects.get(pk=pk)
    profile = user.profile  # onetoone relationship
    sites = profile.site.all()  # objects.all()할 필요없이 이미 site에 모델 객체들이 있음
    posts = user.post.all()

    context = {
        'profile': profile,
        'sites': sites,
        'posts': posts,
    }

    return render(request, 'myprofile/profile_detail.html', context)


# pk1 - post_user(다른 사람의 포스트도 본다), pk2 - post
# def post_detail(request, user_pk, post_pk):
#     user = User.objects.get(pk=user_pk)
#     post = user.post.get(pk=post_pk)
#
#     context = {
#         'post': post,
#     }
#
#     return render(request, 'myprofile/post_detail.html', context)


# 해당 user의 bookmark_list
def bookmark_list(request, pk):
    user = User.objects.get(pk=pk)
    bookmarks = user.bookmark.all()

    context = {
        'bookmarks': bookmarks,
    }

    return render(request, 'myprofile/bookmark_list.html', context)
