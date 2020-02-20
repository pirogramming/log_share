from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth import login as auth_login, update_session_auth_hash
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from accounts.forms import SignupModelForm, CreateUserForm, password_changeForm
from myprofile.models import Profile
from django.urls import reverse_lazy
from django.contrib import messages


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('myprofile:profile_detail', user.pk)
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

        if user_form.is_valid():
            user = user_form.save()
            auth_login(request, user)  # 로그인 처리
            return redirect('accounts:signup_profile')

    elif request.method == "GET":
        user_form = CreateUserForm()

    return render(request, 'accounts/signup.html', {
        'user_form': user_form,
    })


def signup_profile(request):
    if request.method == "POST":
        profile_form = SignupModelForm(
            request.POST,
            request.FILES,
        )

        if profile_form.is_valid():
            user = request.user
            profile = Profile.objects.create(
                user=user,
                name=user.last_name + user.first_name,
                department=profile_form.cleaned_data['department'],
                description=profile_form.cleaned_data['description'],
                naver=profile_form.cleaned_data['naver'],
                daum=profile_form.cleaned_data['daum'],
                github=profile_form.cleaned_data['github'],
                photo=profile_form.cleaned_data['photo'],
                other_url=profile_form.cleaned_data['other_url'],
                interested_tag=profile_form.cleaned_data['interested_tag'],
            )
            return redirect('myprofile:profile_detail', user.pk)

    elif request.method == "GET":
        profile_form = SignupModelForm()

    return render(request, 'accounts/signup_profile.html', {
        'profile_form': profile_form,
    })

#비밀번호 변경
def password_change(request):
    if request.method == 'POST':
        password_change_form = password_changeForm(request.user, request.POST)
        if password_change_form.is_valid():
            # 비번 변경 후 자동 로그인 추가
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            # 여기까지
            return redirect('/', request.user.username)

    else:
        password_change_form = password_changeForm(request.user)
    return render(request, 'accounts/password_change_form.html', {
        'password_change_form': password_change_form
    })


class MyPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('accounts:password_reset')
    template_name = 'accounts/password_reset_form.html'

    def form_valid(self, form):
        messages.info(self.request, '암호 변경 메일을 발송했습니다. 해당 메일로 가서 메일을 확인해주세요.')
        return super().form_valid(form)


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('accounts:after_reset')
    template_name = 'accounts/password_reset_confirm.html'

    def form_valid(self, form):
        return super().form_valid(form)


def after_reset(request):
    return render(request, 'accounts/after_reset.html')