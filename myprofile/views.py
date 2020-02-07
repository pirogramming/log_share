from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse

from myprofile.models import BookMark

@login_required
def profile_detail(request, pk):
    user = User.objects.get(pk=pk)
    profile = user.user_profile  # onetoone relationship
    posts = user.user_post.all()

    context = {
        'profile': profile,
        'posts': posts,
    }

    return render(request, 'myprofile/profile_detail.html', context)


# 해당 user의 bookmark_list
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
