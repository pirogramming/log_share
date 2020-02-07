from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth

from accounts.forms import SignupModelForm, CreateUserForm
from myprofile.models import Profile

from django.contrib.auth.forms import UserCreationForm


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'accounts/login.html', {'error': 'login error'})
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def signup(request):
    if request.method == "POST":
        user_form = CreateUserForm(request.POST)
        profile_form = SignupModelForm(
            request.POST,
            request.FILES,
        )

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            profile = Profile.objects.create(
                user=user,
                name=user.last_name+user.first_name,
                department=profile_form.cleaned_data['department'],
                description=profile_form.cleaned_data['description'],
                naver=profile_form.cleaned_data['naver'],
                daum=profile_form.cleaned_data['daum'],
                github=profile_form.cleaned_data['github'],
                photo=profile_form.cleaned_data['photo'],
                other_url=profile_form.cleaned_data['other_url'],
                interested_tag=profile_form.cleaned_data['interested_tag'],
            )
            return redirect('/')

    elif request.method == "GET":
        user_form = CreateUserForm()
        profile_form = SignupModelForm()

    return render(request, 'accounts/signup.html', {
        'user_form':user_form,
        'profile_form': profile_form,
    })
