from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth

from accounts.forms import SignupForm
from myprofile.models import Profile


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
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password1"],
                last_name=request.POST["last_name"],
                first_name=request.POST["first_name"],
                email=request.POST["email"],
            )

        form = SignupForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            profile = Profile.objects.create(
                user=user,
                name=user.last_name+user.first_name,
                department=form.cleaned_data['department'],
                description=form.cleaned_data['description'],
                naver=form.cleaned_data['naver'],
                daum=form.cleaned_data['daum'],
                github=form.cleaned_data['github'],
                photo=form.cleaned_data['photo'],
                other_url=form.cleaned_data['other_url'],
                interested_tag=form.cleaned_data['interested_tag'],
            )
            return redirect('/')

    elif request.method == "GET":
        form = SignupForm()

    return render(request, 'accounts/signup.html', {
        'form': form,
    })