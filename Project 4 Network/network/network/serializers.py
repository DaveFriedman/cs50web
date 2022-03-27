from .models import User, Post, Like, Follow
from rest_framework.serializers import *


class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class PostSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['body']
