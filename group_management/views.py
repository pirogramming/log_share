from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
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
            group = CustomGroup.objects.create(
                name=form.cleaned_data['name'],
                category=form.cleaned_data['category'],
                notes=form.cleaned_data['notes'],
                is_searchable=form.cleaned_data['is_searchable'],
            )

            content_type = ContentType.objects.get(app_label='group_management', model='CustomGroup')
            codename = 'can_manage_'+str(group.id)
            print('codename: ', codename)
            permission = Permission.objects.create(codename=codename,
                                                   name=codename,
                                                   content_type=content_type)
            manager = User.objects.get(username=request.user)
            group.permissions.add(permission)
            group.user_set.add(manager)
            # manager.groups.add(group)
            manager.user_permissions.add(permission) # manager.has_perms('can_manage_groupid') = True

            return redirect('group_management:detail_group', group.pk)

    else:
        form = GroupForm(
            request.user,  # 여기로 get타고 들어와서 request.POST 빼버림.
        )
    return render(request, 'group_management/create_group.html', {
        'form': form,
    })


def update_group(request, pk):
    group = get_object_or_404(CustomGroup, id=pk)
    if request.method == 'POST':
        form = GroupForm(
            request.user,
            request.POST,
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
    _user = get_object_or_404(User, username=request.user)
    _user_id = _user.id
    try:
        request_message = GroupRequest.objects.create(
            group_id=pk,
            sender_id=_user_id,
        )
    except IntegrityError: # 이미 요청을 보낸 상태일 경우, 새로운 요청 생성하지 않고 원래 페이지로 이동.
        return redirect('group_management:detail_group', pk)

    return redirect('group_management:request_to', pk)


def request_to(request, pk):
    request_messages = GroupRequest.objects.filter(group_id=pk)
    request_messages.filter(Q(status=False) | Q(status=True)).delete()
    context = {
        'messages': request_messages,
    }
    return render(request, 'group_management/request_to.html', context)


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




