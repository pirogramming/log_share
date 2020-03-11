from django.contrib.auth.decorators import login_required
import simplejson as json
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
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
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# from .serializers import UserSerializer, GroupSerializer

### Rest API 파트 ###

# class UserViewSet(viewsets.ModelViewSet):
#     '''
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
from .utils import remove_all_tags_without_objects, tag_count_check


class Search(APIView):

    def get(self, request, format=None):
        # get의 첫번째 인자는 어떤 variable인지, 두번째인자는 default값
        print(request.query_params)
        tags = request.query_params.get('tags', None).split(",")
        # 표시할 검색결과가 있을 때
        if tags is not None:
            posts = Post.objects.filter(tags__name__in=tags).distinct()
            posts_data = serializers.PostSerializer(posts, many=True)
            for post in posts_data.data:
                # from taggit.models import Tag
                # tag_names = [tag.name for tag in Tag.objects.all()]
                # want = tag_names
                # print('')
                # print(want)
                # print('')
                pass

            post_writer = User.objects.get(id=post['user']).user_profile.name

            context = {
                # 'post_data': posts_data,
                'posts_data': posts_data.data,
                'post_writer': post_writer,
            }

            return render(request, 'post/searched_post_list.html', context)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


### Rest API 끝 ###


def post_create(request):
    context = {}
    if request.method == 'POST':
        # 포스트모델폼을 이용하여 정보를 받아온다.
        postform = PostModelForm(request.POST, request.FILES)
        if postform.is_valid():
            post = postform.save(commit=False)
            # 포스트모델폼의 정보가 유효하면, post에 할당한 뒤 FK를 접속한 유저로 지정하여 저장한다.
            post.user = request.user
            # DB에 저장되어서 pk가 생기지 않으면 post.tags에 접근할 수 없기 때문에 어쩔수 없이 저장...
            if post.is_valid_date:
                post.save()
            else:
                # todo 에러메시지?
                return
            # tag개수(최대10개) 제한
            tag_count_check(request, post)
            return redirect('myprofile:profile_detail', request.user.pk)
        else:
            # todo 에러메세지
            return
    else:
        postform = PostModelForm()
        context = {
            'postform': postform,
        }
    return render(request, 'post/post_create.html', context)


# pk: post_pk
def post_detail(request, pk):
    try:
        post = Post.objects.get(id=pk)
    except ObjectDoesNotExist:
        post = None
    user = post.user  # 해당 포스트의 user

    bm = request.user.user_bookmark.filter(post=post)


    context = {
        'post': post,
        'user': user,
        'bm': bm,
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
            post = postform.save(commit=False)
            if post.is_valid_date:
                post = postform.save()
                # tag개수(최대10개) 제한
                tag_count_check(request, post)
            else:
                # todo 에러메시지?
                return
        return redirect('post:post_detail', post.pk)


def post_delete(request):
    pk = request.POST.get('pk', None)
    post = Post.objects.get(id=pk)
    if request.method == "GET":
        return redirect('post:post_detail', post.pk)
    elif request.method == 'POST':
        if request.user == post.user:
            post.delete()
            remove_all_tags_without_objects()
            return redirect('myprofile:profile_detail', request.user.pk)


# pk: post_pk, 해당 post의 bookmark
@login_required
@require_POST  # 해당 뷰는 POST method 만 받는다.
def post_bookmark(request):
    pk = request.POST.get('pk', None)
    post = get_object_or_404(Post, pk=pk)

    bookmark, bookmark_created = BookMark.objects.get_or_create(user=request.user, post=post)
    # 기존에 있는 북마크이면 북마크 취소하기
    if not bookmark_created:
        bookmark.delete()
        message = "북마크가 취소되었습니다."
        img_url = "/media/bookmark_off.jpg"
    else:
        message = "북마크되었습니다."
        img_url = "/media/bookmark_on.jpg"
    context = {
        'bookmark_count': post.bookmark.count(),
        'message': message,
        'img_url': img_url,

    }
    return HttpResponse(json.dumps(context),
                        content_type="application/json")  # context를 json 타입으로(json.dumps() - string일 때 괜찮고,


# 활동보기 - 그룹에 속한 사용자들의 게시글 리스트
def post_list(request):
    user = request.user
    post_list = Post.objects.none()  # Queryset 초기화 : <QuerySet []>

    for group in user.user_groups.all():  # request.user의 그룹들 중에서
        for group_user in group.members.all():  # 그 그룹에 속한 user
            if group_user != user:
                post_list |= group_user.user_post.all()  # add QuerySet

    post_list = post_list.order_by('-start_date', '-end_date')

    bm_list = user.user_bookmark.all()
    bm_post_list = []
    for bm in bm_list:
        bm_post_list.append(bm.post_id)

    paginator = Paginator(post_list, 4)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)  # 해당 페이지의 포스트(post_list)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
        'bm_post_list': bm_post_list,
    }

    return render(request, 'post/post_list.html', context)


# 활동보기 무한스크롤 ajax
def post_list_ajax(request):
    user = request.user
    post_list = Post.objects.none()  # Queryset 초기화 : <QuerySet []>

    for group in user.user_groups.all():  # request.user의 그룹들 중에서
        for group_user in group.members.all():  # 그 그룹에 속한 user
            if group_user != user:
                post_list |= group_user.user_post.all()  # add QuerySet

    post_list = post_list.order_by('-start_date', '-end_date')
    paginator = Paginator(post_list, 4)
    page = request.POST.get('page')  # 현재 페이지 숫자

    bm_list = user.user_bookmark.all()  # user의 북마크들
    bm_post_list = []
    for bm in bm_list:
        bm_post_list.append(bm.post_id)  # user의 북마크의 포스트 리스트

    try:
        posts = paginator.page(page)  # 해당 페이지의 포스트(post_list) - Page 객체
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts': posts,
        'bm_post_list': bm_post_list,
    }

    return render(request, 'post/post_list_ajax.html', context)


# 프로필_무한스크롤 ajax
def profile_post_list_ajax(request):
    pk = request.POST.get('pk', None)
    user = User.objects.get(pk=pk)  # 프로필의 user

    post_list = user.user_post.order_by('-start_date', '-end_date')
    paginator = Paginator(post_list, 2)
    page = request.POST.get('page')  # ajax로부터 POST 타입을 전달받음

    try:
        posts = paginator.page(page)  # 해당 페이지의 포스트(post_list)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    print(page, posts)
    print('--')
    context = {
        'posts': posts
    }
    return render(request, 'post/myprofile_post_list_ajax.html', context)  # ajax_datatype => dataType: 'html'
