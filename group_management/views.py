from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView

from group_management.forms import GroupForm, RequestWithCodeForm
from group_management.models import CustomGroup, GroupRequest


@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(
            request.user,
            request.POST,
        )
        if form.is_valid():
            group = CustomGroup.objects.create(
                manager=request.user,
                group_name=form.cleaned_data['group_name'],
                group_category=form.cleaned_data['group_category'],
                notes=form.cleaned_data['notes'],
                is_searchable=form.cleaned_data['is_searchable'],
                access_code=form.cleaned_data['access_code'],
            )
            group.members.add(request.user)
            return redirect('group_management:manage_detail', group.pk)
    else:
        form = GroupForm(
            request.user,  # 여기로 get타고 들어와서 request.POST 빼버림.
        )
    return render(request, 'group_management/create_group.html', {
        'form': form,
    })


@login_required
def manage_list(request):
    groups = request.user.user_manage_groups.all()
    context = {
        'groups': groups,
    }
    return render(request, 'group_management/list_group_for_manager.html', context)


def manage_detail(request, pk):
    group = get_object_or_404(CustomGroup, id=pk)
    try:
        if request.user != group.manager:
            raise NotImplementedError
    except NotImplementedError:
        return HttpResponse(404)
    context = {
        'group': group,
    }
    return render(request, 'group_management/detail_group_for_manager.html', context)


def update_group(request, pk):
    group = get_object_or_404(CustomGroup, id=pk)
    try:
        if request.user != group.manager:
            raise NotImplementedError
    except NotImplementedError:
        return redirect('group_management:manage_detail', pk)
    if request.method == 'POST':
        form = GroupForm(
            request.user,
            request.POST,
            instance=group,
        )
        if form.is_valid():
            group = form.save()
            return redirect('group_management:manage_detail', pk)

    else:
        form = GroupForm(
            request.user,
            instance=group
        )
    return render(request, 'group_management/create_group.html', {
        'form': form,
    })


@login_required()
def request_to(request):
    manager = request.user
    groups = manager.user_manage_groups.all()
    context = {}
    for group in groups:
        request_messages = GroupRequest.objects.filter(group=group)
        request_messages.filter(Q(status=False) | Q(status=True)).delete()
        context = {
            'messages': request_messages,
        }
    return render(request, 'group_management/request_to.html', context)


def allow_request(request, pk):
    print('aaa')
    message = get_object_or_404(GroupRequest, id=pk)
    sender = message.sender
    group = message.group
    group.members.add(sender)
    print(group.members.all())
    GroupRequest.objects.filter(id=pk).delete()
    return JsonResponse({
        'messages': GroupRequest.objects.all(),
    })


def manage_members(request, pk):
    group = get_object_or_404(CustomGroup, id=pk)
    try:
        if request.user != group.manager:
            raise NotImplementedError
    except NotImplementedError:
        return HttpResponse(404)
    members = group.members.all()
    print(members)

    context = {
        'group': group,
        'members': members,
    }
    return render(request, 'group_management/manage_members.html', context)


def all_group(request):
    groups = CustomGroup.objects.all()
    context = {
        'groups': groups,
    }
    return render(request, 'group_management/all_group.html', context)


def detail_group(request, pk):
    group = get_object_or_404(CustomGroup, id=pk)
    context = {
        'group': group,
    }
    return render(request, 'group_management/detail_group.html', context)


def request_group(request, pk):
    group = get_object_or_404(CustomGroup, id=pk)
    if request.user in group.members.all():
        return redirect('group_management:detail_group', pk)
    try:
        request_message = GroupRequest.objects.create(
            group=group,
            sender=request.user,
        )
    except IntegrityError: # 이미 요청을 보낸 상태일 경우, 새로운 요청 생성하지 않고 원래 페이지로 이동.
        return redirect('group_management:detail_group', pk)
    return redirect('group_management:request_from', request.user.id)


def request_withcode(request):
    if request.method == 'POST':
        form = RequestWithCodeForm(
            request.POST,
        )

        group = get_object_or_404(
            CustomGroup,
            Q(group_name=form.data['group_name']) & Q(access_code=form.data['access_code'])
        )
        print(group)
        return redirect('group_management:request_group', group.pk)
    else:
        form = RequestWithCodeForm()
    return render(request, 'group_management/request_withcode.html', {
        'form': form,
    })


def request_from(request, pk):
    request_messages = GroupRequest.objects.filter(sender_id=pk)
    request_messages.filter(Q(status=False) | Q(status=True)).delete()
    context = {
        'messages': request_messages,
    }
    return render(request, 'group_management/request_from.html', context)


def add_member(user_id, group_id):
    group = get_object_or_404(CustomGroup, id=group_id)
    user = get_object_or_404(User, id=user_id)
    group.user_set.add(user)
    return group.user_set.all()


def del_member(user_id, group_id):
    group = get_object_or_404(CustomGroup, id=group_id)
    user = get_object_or_404(User, id=user_id)
    group.user_set.remove(user)
    return group.user_set.all()



