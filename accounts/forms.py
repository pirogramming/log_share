from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import FileInput

from myprofile.models import Profile


class CreateUserForm(UserCreationForm):  # 내장 회원가입 폼을 상속받아서 확장한다.
    email = forms.EmailField(required=True)  # 이메일 필드 추가
    last_name = forms.CharField(required=True, max_length=10)
    first_name = forms.CharField(required=True, max_length=10)

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "last_name", "first_name", "email")
        labels={"username":"아이디","last_name":"성","first_name":"이름","email":"이메일"}

    def save(self, commit=True):  # 저장하는 부분 오버라이딩
        user = super(CreateUserForm, self).save(commit=False)  # 본인의 부모를 호출해서 저장하겠다.
        user.email = self.cleaned_data["email"]
        user.last_name = self.cleaned_data["last_name"]
        user.first_name = self.cleaned_data["first_name"]

        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()  # settings.py에서 설정된 User 모델을 갖고옴
        fields = ['last_name', 'first_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        self.fields.get('password').label = ''
        self.fields.get('password').help_text = ''
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')


class SignupModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('department', 'description', 'photo', 'interested_tag', 'naver', 'daum', 'github', 'other_url')
        widgets = {
            'photo': FileInput(),
        }

        help_texts = {
            'interested_tag': '띄어쓰기 없이 반점(,)으로 태그를 구별하여 입력하세요.'
        }

        def __init__(self, *args, **kwargs):
            super(SignupModelForm, self).__init__(*args, **kwargs)
            self.fields['photo'].widget.attrs = {'id': 'selectedFile'}


class password_changeForm(PasswordChangeForm):  # 내장 회원가입 폼을 상속받아서 확장한다.
    class Meta:
        model = User
        fields = ("old_password","new_password1","new_password2")
        labels={"old_password":"기존 비밀번호","new_password1":"새 비밀번호","new_password2":"새 비밀번호 확인"}
