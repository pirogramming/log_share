from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from .models import User


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].validators = [validate_email]
        self.fields['username'].help_text = 'Enter Email Format.'
        self.fields['username'].label = 'Email'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = user.username
        if commit:
            user.save()
        return user

    class Meta(UserCreationForm.Meta):
        model = User


    '''
    def clean_username(self):
        value = self.cleaned_data.get('username')
        if value:
            validate_email(value)
        return value
    '''