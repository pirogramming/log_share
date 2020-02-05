from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post

def post_detail(request, user_pk, post_pk):
    user = User.objects.get(pk=user_pk)
    post = user.post.get(pk=post_pk)

    context = {
        'post': post,
    }

    return render(request, 'post/post_detail.html', context)

# todo     pk: post_pk
def post_bookmark(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post_bookmark, post_bookmark_created = post.bookmark_user_set.get_or_create(user=request.user)

    if not post_bookmark_created:
        post_bookmark.delete()  #기존에 북마크 누른 user이면 삭제

    return redirect('post:post_detail')
