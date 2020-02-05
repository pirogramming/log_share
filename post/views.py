from django.contrib.auth.models import User
from django.shortcuts import render

def post_detail(request, user_pk, post_pk):
    user = User.objects.get(pk=user_pk)
    post = user.post.get(pk=post_pk)

    context = {
        'post': post,
    }

    return render(request, 'post/post_detail.html', context)
