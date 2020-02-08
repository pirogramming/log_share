from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from accounts.forms import SignupModelForm, CustomUserChangeForm
from myprofile.models import BookMark, Profile


# <<<<<<<<<<<<<<user_pk>>>>>>>>>>>>>>
@login_required
def profile_detail(request, pk):
    user = User.objects.get(pk=pk)
    profile = user.user_profile  # user -> profile
    posts = user.user_post.all()  # user -> post

    context = {
        'profile': profile,
        'posts': posts,
    }

    return render(request, 'myprofile/profile_detail.html', context)


@login_required
def profile_edit(request, pk):
    user = User.objects.get(pk=pk)
    profile = user.user_profile

    if request.method == "POST":
        user_change_form = CustomUserChangeForm(
            request.POST,
            instance=user
        )
        profile_form = SignupModelForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_change_form.is_valid() and profile_form.is_valid():
            user_change_form.save()
            profile = profile_form.save()
            profile.name = request.user.last_name + request.user.first_name  # user의 이름 -> profile.name
            profile = profile.save()

            return redirect('myprofile:profile_detail', request.user.pk)

    elif request.method == "GET":
        user_change_form = CustomUserChangeForm(instance=user)
        profile_form = SignupModelForm(instance=profile)

    return render(request, 'myprofile/profile_edit.html', {
        'user_change_form': user_change_form,
        'profile_form': profile_form,
    })


# user_pk / 해당 user의 bookmark_list
def bookmark_list(request, pk):
    user = User.objects.get(pk=pk)
    bookmarks = user.user_bookmark.all()

    context = {
        'bookmarks': bookmarks,
    }

    return render(request, 'myprofile/bookmark_list.html', context)


# pk : bookmark.pk
def bookmark_delete(request, pk):
    bookmark = BookMark.objects.get(pk=pk)
    bookmark.delete()

    return redirect('myprofile:bookmark_list', bookmark.user.pk)
