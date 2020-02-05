from django.forms import ModelForm
from .models import Post


class PostModelForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__' #여기서 user는 request.user로 자동지정해주고 필드에서 빼야함

