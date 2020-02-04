from django.contrib.auth import get_user_model
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
    request_message = GroupRequest.objects.create(
        group_id=pk,
        sender_id=_user_id,
    )
    return redirect('group_management:detail_group')


def request_list(request, pk):
    request_messages = GroupRequest.objects.filter(group_id=pk)
    context = {
        'messages': 'request_messages',
    }
    return render(request, 'group_management/request_list.html', context)