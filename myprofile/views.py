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

def post_list(request):
    posts = Post.objects.all() # 실제로는 내가 속한 그룹 인원들의 게시물만 가져와야함.
    #posts = Post.objects.filter(tags__name__in=["찾을태그"])
    context = {
        'posts': posts,
    }

    return render(request, 'myprofile/post_list.html', context)


def post_create(request):

    if request.method == 'POST':
        #포스트모델폼을 이용하여 정보를 받아온다.
        postform = PostModelForm(request.POST, request.FILES)
        if postform.is_valid():
            #포스트모델폼의 정보가 유효하면, post에 할당한 뒤 FK를 접속한 유저로 지정하여 저장한다.
            post = postform.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('myprofile:post_list')
    else:
        postform = PostModelForm()
        context = {
            'postform': postform,
        }
    return render(request, 'myprofile/post_create.html', context)

def post_detail(request,pk):
    post = Post.objects.get(id=pk)
    context = {
        'post': post,
    }
    return render(request,'myprofile/post_detail.html', context)

def post_update(request,pk):
    post = Post.objects.get(id=pk)
    if request.method == "GET":
        postform = PostModelForm(instance=post)
        context = {
            'postform':postform,
        }
        return render(request,'myprofile/post_update.html', context)
    else:
        postform = PostModelForm(request.POST, request.FILES, instance=post)
        if postform.is_valid():
            post = postform.save()

            return redirect('myprofile:post_detail', post.pk)

def post_delete(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == "GET":
        return redirect('myprofile:post_detail',post.pk)
    elif request.method == 'POST':
        if request.user == post.user:
            post.delete()
            return redirect('myprofile:post_list')
