from .models import CustomGroup
from django import forms
from django.contrib.auth import get_user_model


class GroupForm(forms.ModelForm):
    class Meta:
        model = CustomGroup
        fields = ('name', 'category', 'notes', 'is_searchable',)
        labels = {
            'name': '이름',
            'category': '카테고리',
            'notes': '그룹 설명',
            'is_searchable': '검색허용',
        }

    def __init__(self, username, *args, **kwargs):# -> object:
        super(GroupForm, self).__init__(*args, **kwargs)
