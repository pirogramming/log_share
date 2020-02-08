from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from myprofile.models import Profile


class CreateUserForm(UserCreationForm):  # 내장 회원가입 폼을 상속받아서 확장한다.
    email = forms.EmailField(required=True)  # 이메일 필드 추가
    last_name = forms.CharField(required=True, max_length=10)
    first_name = forms.CharField(required=True, max_length=10)

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "last_name", "first_name", "email")

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

    def save(self, commit=True):
        pass


class SignupModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('department', 'description', 'photo', 'interested_tag', 'naver', 'daum', 'github', 'other_url')
