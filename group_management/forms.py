from .models import CustomGroup
from django import forms
from django.contrib.auth import get_user_model


class GroupForm(forms.ModelForm):

    class Meta:
        model = CustomGroup
        fields = ('group_name', 'group_category', 'notes', 'is_searchable', 'access_code')
        labels = {
            'group_name': '그룹명',
            'group_category': '카테고리',
            'notes': '그룹 설명',
            'is_searchable': '검색 허용',
            'access_code': '그룹 검색 코드'
        }

    def __init__(self, username, *args, **kwargs):# -> object:
        super(GroupForm, self).__init__(*args, **kwargs)


class RequestWithCodeForm(forms.Form):
    group_name = forms.CharField(label='그룹명', max_length=50)
    access_code = forms.CharField(label='그룹 접근 코드')

    def __init__(self, *args, **kwargs):
        super(RequestWithCodeForm, self).__init__(*args, **kwargs)
        self.fields['group_name'].widget.attrs.update({
            'class': 'group_name_input',
            'placeholder': '그룹명'
        })
        self.fields['access_code'].widget.attrs.update({
            'class': 'group_access_code_input',
            'placeholder': '가입코드'
        })
