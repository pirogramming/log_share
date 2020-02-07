from django.forms import ModelForm
from .models import Post


class PostModelForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            'category','title','contents','reference','start_date','end_date','photo','tags','score'
        ]
        '''
        #todo 사진 변경시에 원래 있던 사진 삭제를 자동으로 해주는 기능.
        templates/django/forms/widgets/clearable_file_input.html 에서 checkbox='checked', input='hidden' 만들었어서 상관없긴한데..
        결국에 시간대별로 uuid 지정되어서 원래 있던 파일 삭제는 링크걸리지 않은 파일을 찾는 함수 만들어서 주기적으로 해줄수밖에 없는듯.
        '''

