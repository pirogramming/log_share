from django import forms
from django.contrib.auth.forms import UserCreationForm
from myprofile.models import Profile

class SignupForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'department', 'description', 'photo', 'interested_tag', 'naver', 'daum', 'github', 'other_url')
