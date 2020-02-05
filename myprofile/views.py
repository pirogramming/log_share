from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse

from myprofile.models import BookMark


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


# 해당 user의 bookmark_list
def bookmark_list(request, pk):
    user = User.objects.get(pk=pk)
    bookmarks = user.bookmark.all()

    context = {
        'bookmarks': bookmarks,
    }

    return render(request, 'myprofile/bookmark_list.html', context)


# pk : bookmark.pk
def bookmark_delete(request, pk):
    bookmark = BookMark.objects.get(pk=pk)
    bookmark.delete()

    return redirect(reverse('myprofile:bookmark_list', kwargs={'pk': bookmark.user.pk}))
