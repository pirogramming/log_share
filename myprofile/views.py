from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from myprofile.forms import PostModelForm
from myprofile.models import Post, Profile


def profile_detail(request,pk):
    profile = get_object_or_404(Profile, id=pk)
    sites = profile.site.all()
    posts = profile.user.post.all()


    context={
        'profile': profile,
        'sites': sites,
        'posts': posts,
    }

    return render(request,'myprofile/profile_detail.html',context)


def posting_create(request):
    post = Post(user=request.user)
    if request.method == 'POST':
        form = PostModelForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('myprofile:posting_list')
    else:
        form = PostModelForm(instance=post)

        context = {
            'form': form,
        }
    return render(request, 'myprofile/posting_create.html', context)

def posting_list(request):
    posts = Post.objects.all() # 실제로는 내가 속한 그룹 인원들의 게시물만 가져와야함.

    context = {
        'posts': posts,
    }

    return render(request, 'myprofile/posting_list.html', context)
