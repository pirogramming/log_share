from django.contrib.auth.models import User, Group
from .models import Post
from rest_framework import serializers

# # User 모델에서 user,username, email, groups 필드를 DB에서 가져와 Json으로 변경하기 위하여.
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'groups']
#
# # Group 모델에서 url, name 필드를 DB에서 가져와 Json으로 변경하기 위하여.
# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']

# Post 모델에서 특정 필드들에 대하여 DB 정보들을 검색해주고, Json으로 변경해준다.
class PostSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['id','category','title','score','user','start_date','end_date', 'tags']
        #fields에 user를 가져오려고 하면 hyperlinkModelSerializer 에러가 뜬다.
