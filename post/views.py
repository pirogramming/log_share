from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.serializers import json
from django.http import HttpResponse
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


# pk: post_pk, 해당 post의 bookmark
@login_required
def post_bookmark(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # post.bookmark_user_set : 해당 post의 bookmarks
    bookmark, bookmark_created = BookMark.objects.get_or_create(user=request.user, post=post)

    # 기존에 있는 북마크이면 북마크 취소하기
    if not bookmark_created:
        bookmark.delete()

    return redirect(reverse('post:post_detail', kwargs={'user_pk': post.user.pk, 'post_pk': post.pk}))


# todo bookmark ajax - POST method 만날 때 실행되는 뷰
# def post_bookmark(request):
#     pk = request.POST.get('pk', None)
#     post = get_object_or_404(Post, pk=pk)
#     bookmark, bookmark_created = BookMark.objects.get_or_create(user=request.user, post=post)
#
#     if not bookmark_created:
#         bookmark.delete()
#         message = "북마크 취소"
#     else:
#         message = "북마크"
#
#     context = {
#         'bookmark_count': post.bookmark.count(),
#         'message': message,
#     }
#
#     return HttpResponse(json.dumps(context), content_type="post/json")  # context를 json 타입으로
