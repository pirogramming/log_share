from django.forms import ModelForm
from .models import Post, Tag


class PostModelForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

class TagModelForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['word']
