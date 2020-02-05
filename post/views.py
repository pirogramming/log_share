from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from myprofile.models import BookMark
from django.urls import reverse



def post_detail(request, user_pk, post_pk):
    user = User.objects.get(pk=user_pk)
    post = user.post.get(pk=post_pk)

    context = {
        'post': post,
    }

    return render(request, 'post/post_detail.html', context)


# todo   bookmark - count
# def post_bookmark(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     # bookmark 누른 user 저장 - post_bookmark_user
#     post_bookmark_user, post_bookmark_created = post.bookmark_user_set.get_or_create(id=request.user.pk)
#
#     if not post_bookmark_created:
#         post_bookmark_user.delete()  # 기존에 북마크 누른 user이면 삭제
#
#     return redirect('post:post_detail')


# pk: post_pk, 해당 post의 bookmark
@login_required
def post_bookmark(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # post.bookmark_user_set : 해당 post의 bookmarks
    bookmark, bookmark_created = BookMark.objects.get_or_create(user=request.user, post=post)

    #기존에 있는 북마크이면 삭제하기
    if not bookmark_created:
        bookmark.delete()

    return redirect(reverse('post:post_detail', kwargs={'user_pk':post.user.pk, 'post_pk':post.pk}))
