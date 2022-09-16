from api.models import Posts
from rest_framework import serializers
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)  # 1 --> 2 in views
    class Meta:
        model = Posts
        exclude = ("date", )
        # fields=["title","description","image","user"]

    def create(self, validated_data):  # 3
        user = self.context.get('usr')
        return Posts.objects.create(**validated_data, user=user)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

