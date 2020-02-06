from django.contrib.auth.models import User, Group
from rest_framework import serializers


# serializer란 models 객체와 querysets 같은 복잡한 데이터를 JSON, XML과 같은 native 데이터로 바꿔주는 역할을 한다.
# 아래에서는 HyperlinkedModelSerializer라는 serializer를 사용한다.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

# class PostSerializer(serializers.ModelSerializer):
