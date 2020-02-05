from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from group_management.forms import GroupForm
from group_management.models import CustomGroup, GroupRequest


def create_group(request):
    if request.method == 'POST':
        form = GroupForm(
            request.user,
            request.POST,
        )
        if form.is_valid():
            # groups = CustomGroup.objects.all()
            group = CustomGroup.objects.create(
                name=form.cleaned_data['name'],
                category=form.cleaned_data['category'],
                notes=form.cleaned_data['notes'],
                is_searchable=form.cleaned_data['is_searchable'],
            )
            return redirect('group_management:detail_group', group.pk)

    else:
        form = GroupForm(
            request.user,  # 여기로 get타고 들어와서 request.POST 빼버림.
            instance=request.user,
        )
    return render(request, 'group_management/create_group.html', {
        'form': form,
    })


def update_group(request, pk):
    group = CustomGroup.objects.all().filter(id=pk)[0]
    if request.method == 'POST':
        if group.name != request.POST['name']:
            group.name = request.POST['name']

        if request.POST['is_searchable'] == 'on':
            _is_searchable = True
        else:
            _is_searchable = False

        group = CustomGroup.objects.all().filter(id=pk).update(
            category=request.POST['category'],
            notes=request.POST['notes'],
            is_searchable=request.POST['is_searchable'],
        )
        return redirect('group_management:detail_group', pk)

    else:
        form = GroupForm(
            request.user,  # 여기로 get타고 들어와서 request.POST 빼버림.
            instance=request.user,
            initial={
                'name': group.name,
                'category': group.category,
                'notes': group.notes,
                'is_searchable': group.is_searchable,
            },
        )
    return render(request, 'group_management/create_group.html', {
        'form': form,
    })


def list_group(request):
    groups = CustomGroup.objects.all()
    context = {
        'groups': groups,
    }
    return render(request, 'group_management/list_group.html', context)


def detail_group(request, pk):
    group = get_object_or_404(CustomGroup, id=pk)
    context = {
        'group': group,
    }
    return render(request, 'group_management/detail_group.html', context)


def request_group(request, pk):
    _group = get_object_or_404(CustomGroup, id=pk)
    users = get_user_model()
    _user_id = users.objects.filter(username=request.user)[0].id
    try:
        request_message = GroupRequest.objects.create(
            group_id=pk,
            sender_id=_user_id,
        )
    except IntegrityError: # 이미 요청을 보낸 상태일 경우, 새로운 요청 생성하지 않고 원래 페이지로 이동.
        return redirect('group_management:detail_group', pk)

    return redirect('group_management:request_list', pk)


def request_list(request, pk):
    request_messages = GroupRequest.objects.filter(group_id=pk)
    request_messages.filter(Q(status=False) | Q(status=True)).delete()
    print([request_messages])
    context = {
        'messages': request_messages,
    }
    return render(request, 'group_management/request_list.html', context)


def add_member(user_id, group_id):
    group = CustomGroup.objects.all().filter(id=group_id)[0]
    user = User.objects.all().filter(id=user_id)[0]
    group.user_set.add(user)
    return group.user_set.all()


def del_member(user_id, group_id):
    group = CustomGroup.objects.all().filter(id=group_id)[0]
    user = User.objects.all().filter(id=user_id)[0]
    group.user_set.remove(user)

