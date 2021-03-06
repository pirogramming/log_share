from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from group_management.forms import GroupForm, RequestWithCodeForm
from group_management.models import CustomGroup, GroupRequest
from django.contrib import messages


@login_required
def all_create_group(request):
    if request.method == 'POST':
        form = GroupForm(
            request.user,
            request.POST,
            request.FILES,
        )
        if form.is_valid():
            group = CustomGroup.objects.create(
                manager=request.user,
                group_name=form.cleaned_data['group_name'],
                group_category=form.cleaned_data['group_category'],
                notes=form.cleaned_data['notes'],
                photo=form.cleaned_data['photo'],
                is_searchable=form.cleaned_data['is_searchable'],
                access_code=form.cleaned_data['access_code'],
            )
            group.members.add(request.user)

    groups = request.user.user_groups.all()

    requested_groups = list()
    for group in list(request.user.user_manage_groups.all()):
        temp = GroupRequest.objects.filter(group=group)
        if temp:
            requested_groups.append(group)

    form = GroupForm(
        request.user,  # 여기로 get타고 들어와서 request.POST 빼버림.
    )
    return render(request, 'group_management/create_group.html', {
        'form': form, 'groups': groups, 'requested_groups': requested_groups,
    })


@login_required
@require_POST
def allow_request(request):
    pk = request.POST.get('pk', None)
    message = get_object_or_404(GroupRequest, id=pk)
    sender = message.sender
    group = message.group
    group.members.add(sender)
    GroupRequest.objects.filter(id=pk).delete()
    context = {
        'messages': GroupRequest.objects.filter(group=group)
    }
    return HttpResponse(context)


@login_required
@require_POST
def disallow_request(request):
    pk = request.POST.get('pk', None)
    message = get_object_or_404(GroupRequest, id=pk)
    group = message.group
    GroupRequest.objects.filter(id=pk).delete()
    context = {
        'messages': GroupRequest.objects.filter(group=group)
    }
    return HttpResponse(context)


@login_required
def delete_member(request):
    member_id = request.POST.get('member_id', None)
    member = get_object_or_404(User, id=member_id)
    group_id = request.POST.get('group_id', None)
    now_group = get_object_or_404(CustomGroup, id=group_id)
    # 해당 그룹과 멤버 조인 테이블에서 특정 레코드를 삭제한다.(멤버관계를 삭제한다)
    now_group.members.remove(member)
    context = {
        'group': now_group,
    }
    return HttpResponse(context)


@login_required
def search_group(request):
    user = request.user
    qs = CustomGroup.objects.filter(is_searchable=1)
    q = request.GET.get('q', '')  # GET request의 인자중에 q 값이 있으면 가져오고, 없으면 빈 문자열 넣기
    if q:
        qs = CustomGroup.objects.filter(Q(group_name__icontains=q) & Q(is_searchable=1))
    access_code_form = RequestWithCodeForm()
    context = {
        'groups': qs,
        'access_code_form': access_code_form,
        'q': q,
    }
    return render(request, 'group_management/search_group.html', context)


@login_required
def detail_group(request, pk):
    group = get_object_or_404(CustomGroup, id=pk)

    if request.method == 'POST':
        form = GroupForm(
            request.user,
            request.POST,
            request.FILES,
            instance=group,
        )

        if form.is_valid():
            group = form.save()
            return redirect('group_management:detail_group', pk)

    else:
        form = GroupForm(
            request.user,
            instance=group
        )
    form = GroupForm(
        request.user,
        instance=group,
    )
    group = get_object_or_404(CustomGroup, id=pk)
    q = request.GET.get('q', '')  # GET request의 인자중에 q 값이 있으면 가져오고, 없으면 빈 문자열 넣기
    user = request.user
    messages = GroupRequest.objects.filter(group=group)

    qs = group.members.all()

    if q:
        qs = group.members.filter(Q(username__icontains=q) | Q(user_profile__name__icontains=q))
    context = {
        'group': group,
        'members': qs,
        'messages': messages,
        'form': form,
    }
    return render(request, 'group_management/detail_group.html', context)


@login_required
def request_group(request, pk):
    group = get_object_or_404(CustomGroup, id=pk)  # 요청 보낸 그룹
    # manager = group.manager

    if request.user in group.members.all():
        return redirect('group_management:detail_group', pk)
    try:
        request_message = GroupRequest.objects.create(
            group=group,
            sender=request.user,
        )

    except IntegrityError:  # 이미 요청을 보낸 상태일 경우, 새로운 요청 생성하지 않고 원래 페이지로 이동.
        return redirect('group_management:detail_group', pk)
    return redirect('group_management:detail_group', pk)


@login_required
def request_withcode(request):
    if request.method == 'POST':
        form = RequestWithCodeForm(
            request.POST,
        )
        try:
            group = CustomGroup.objects.get(
                Q(group_name=form.data['group_name']) & Q(access_code=form.data['access_code']))

        except Exception:
            messages.info(request, '입력한 정보와 일치하는 그룹이 존재하지 않습니다.')
            return redirect('group_management:search_group')

        if request.user in group.members.all():
            messages.info(request, '이미 해당 그룹의 멤버입니다.')
            return redirect('group_management:search_group')
        try:
            request_message = GroupRequest.objects.create(
                group=group,
                sender=request.user,
            )
        except IntegrityError:  # 이미 요청을 보낸 상태일 경우, 새로운 요청 생성하지 않고 원래 페이지로 이동.
            messages.info(request, '이미 요청을 한 상태입니다.')
            return redirect('group_management:search_group')

        messages.info(request, '가입신청을 완료했습니다.')
    return redirect('group_management:search_group')


@login_required
def delete_group(request, pk):
    group = get_object_or_404(CustomGroup, id=pk)
    group.delete()
    return redirect('group_management:create_group')


@login_required
def secede_group(request, pk):
    group = get_object_or_404(CustomGroup, id=pk)
    group.members.remove(request.user)
    return redirect('group_management:detail_group', pk)
