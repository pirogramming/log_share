from django.forms import ModelForm
from django.forms.widgets import ClearableFileInput, FileInput
from django_summernote.widgets import SummernoteWidget
from .widgets import starWidget
from .models import Post


class PostModelForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            'category', 'title', 'contents', 'reference', 'start_date', 'end_date', 'photo', 'tags', 'score'
        ]
        widgets = {
            'contents': SummernoteWidget(),
            'score': starWidget,
            'photo': FileInput(),
        }
        help_texts = {
            'tags': '띄어쓰기 없이 반점(,)을 이용하여 태그를 구별하세요. 최대 10개까지 입력됩니다.',
        }
        labels = {
            'tags': '태그',

        }
        '''
                #todo 사진 변경시에 원래 있던 사진 삭제를 자동으로 해주는 기능.
                templates/django/forms/widgets/clearable_file_input.html 에서 checkbox='checked', input='hidden' 만들었어서 상관없긴한데..
                결국에 시간대별로 uuid 지정되어서 원래 있던 파일 삭제는 링크걸리지 않은 파일을 찾는 함수 만들어서 주기적으로 해줄수밖에 없는듯.
        '''

    def __init__(self, *args, **kwargs):
        super(PostModelForm, self).__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs = {'id':'selectedFile'}
