from django.contrib.auth.decorators import login_required
import simplejson as json
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from myprofile.models import BookMark, Profile
from . import serializers
from .forms import PostModelForm
from .models import Post


# from .serializers import UserSerializer, GroupSerializer

### Rest API 파트 ###

# class UserViewSet(viewsets.ModelViewSet):
#     '''
#     API endpoint that allows users to be viewed or edited.
#     '''
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#
# class GroupViewSet(viewsets.ModelViewSet):
#     '''
#     API endpoint that allows groups to be viewed or edited.
#     '''
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer

class Search(APIView):

    def get(self, request, format=None):
        # get의 첫번째 인자는 어떤 variable인지, 두번째인자는 default값
        print(request.query_params)
        tags = request.query_params.get('tags', None).split(",")
        # 표시할 검색결과가 있을 때
        if tags is not None:
            posts = Post.objects.filter(tags__name__in=tags).distinct()
            posts_data = serializers.PostSerializer(posts, many=True)
            # for post in posts_data.data:
            #     want = post
            #     print('')
            #     print(want)
            #     print('')
            #     pass

            context = {
                # 'post_data': posts_data,
                'posts_data': posts_data.data,
                'tags': tags,
            }

            return render(request, 'post/searched_post_list.html', context)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # todo User값과 태그값을 받아올 수 있으면 좋은데..


### Rest API 끝 ###

# def post_list(request):
#     posts = Post.objects.all()  # 실제로는 내가 속한 그룹 인원들의 게시물만 가져와야함.
#     # posts = Post.objects.filter(tags__name__in=["찾을태그"])
#     '''
#     만약 ["찾을태그1","찾을태그2"]식으로 여러개의 태그를 넣어 검색할 경우
#     태그 1과 태그 2를 동시에 가지고 있는 게시물은 두 번 조회될 수 있다(쿼리셋에 2번이나 들어오게 된다)
#     이때는 쿼리문 제일 끝에 .distinct()를 붙여주면 포스트의 중복을 막을 수 있다.
#     '''
#     # qs = str(Post.tags.all()) 이렇게 할 시 포스트 모델에 존재하는 모든 태그를 가져올 수 있다.
#
#     context = {
#         'posts': posts,
#     }
#
#     return render(request, 'post/post_list.html', context)


def post_scroll_list(request, pk):
    profile = Profile.objects.get(pk=pk)
    user = profile.user
    posts = user.user_post.order_by('start_date')
    return render(request, 'post/myprofile_post_list.html', {'posts':posts})
    # paginator = Paginator(posts, 10)
    # page = request.GET.get('page')
    # pageposts = paginator.get_page(page)  # 10개만큼 포스트 출력
    # context = {
    #     'posts': posts,
    #     'pageposts': pageposts,
    # }
    # return render(request, 'post/myprofile_post_list.html')


def post_create(request):
    if request.method == 'POST':
        # 포스트모델폼을 이용하여 정보를 받아온다.
        postform = PostModelForm(request.POST, request.FILES)
        if postform.is_valid():
            # 포스트모델폼의 정보가 유효하면, post에 할당한 뒤 FK를 접속한 유저로 지정하여 저장한다.
            post = postform.save(commit=False)
            post.user = request.user
            post = postform.save()
            return redirect('myprofile:profile_detail', request.user.pk)
    else:
        postform = PostModelForm()
        context = {
            'postform': postform,
        }
    return render(request, 'post/post_create.html', context)


# pk: post_pk
def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    user = post.user  # 해당 포스트의 user

    context = {
        'post': post,
        'user': user,
    }
    return render(request, 'post/post_detail.html', context)


def post_update(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == "GET":
        postform = PostModelForm(instance=post)
        context = {
            'postform': postform,
        }
        return render(request, 'post/post_update.html', context)
    else:
        postform = PostModelForm(request.POST, request.FILES, instance=post)
        if postform.is_valid():
            post = postform.save()
        return redirect('post:post_detail', post.pk)


def post_delete(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == "GET":
        return redirect('post:post_detail', post.pk)
    elif request.method == 'POST':
        if request.user == post.user:
            post.delete()
            return redirect('myprofile:profile_detail', request.user.pk)


@login_required
@require_POST  # 해당 뷰는 POST method 만 받는다.
def post_bookmark(request):
    pk = request.POST.get('pk', None)
    post = get_object_or_404(Post, pk=pk)
    bookmark, bookmark_created = BookMark.objects.get_or_create(user=request.user, post=post)
    # 기존에 있는 북마크이면 북마크 취소하기
    if not bookmark_created:
        bookmark.delete()
        message = "북마크 취소"
    else:
        message = "북마크"

    context = {
        'bookmark_count': post.bookmark.count(),
        'message': message,
    }
    return HttpResponse(json.dumps(context), content_type="application/json")  # context를 json 타입으로
