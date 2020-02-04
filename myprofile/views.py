from django.shortcuts import render
from .models import Profile, BookMark
from django.contrib.auth.models import User


def profile_detail(request, pk):
    user = User.objects.get(pk=pk)
    profile = user.profile
    sites = profile.site.all()  # objects.all()할 필요없이 이미 site에 모델 객체들이 있음

    context = {
        'profile': profile,
        'sites': sites,
    }

    return render(request, 'myprofile/profile_detail.html', context)


# 해당 user의 bookmark_list
def bookmark_list(request, pk):
    user = User.objects.get(pk=pk)
    bookmarks = user.bookmark.all()

    context = {
        'bookmarks': bookmarks,
    }

    return render(request, 'myprofile/bookmark_list.html', context)


def post_list(request, pk):
    pass

#pk1 - post_user, pk2 - post
def post_detail(request, pk1, pk2):
    user = User.objects.get(pk=pk1)
    post = user.post.get(pk=pk2)

    context = {
        'post': post,
    }

    return render(request, 'myprofile/post_detail.html', context)
