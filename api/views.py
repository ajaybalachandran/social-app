from django.shortcuts import render
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from api.serializers import PostSerializer, UserSerializer, CommentModelSerializer
from api.models import Posts
from rest_framework import authentication, permissions
from rest_framework.decorators import action
# Create your views here.

class PostsView(ViewSet):
    # authentication_classes = [authentication.BasicAuthentication]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def list(self, request, *args, **kwargs):
        qs = Posts.objects.all()
        serializer = PostSerializer(qs, many=True)
        return Response(data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(serializer.errors)

    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        qs = Posts.objects.get(id=id)
        serializer = PostSerializer(qs)
        return Response(data=serializer.data)

    def update(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        instance = Posts.objects.get(id=id)
        serializer = PostSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def destroy(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        instance = Posts.objects.get(id=id)
        instance.delete()
        return Response({'msg':'deleted'})


class UsersView(ViewSet):
    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class PostsModelView(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Posts.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):  # 2 --> 3 in serializers
        serializer = PostSerializer(data=request.data, context={'usr': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)

# custom method
    @action(methods=["GET"], detail=False)
    # localhost:8000/api/v2/posts/my_posts/
    def my_posts(self, request, *args, **kwargs):
        user = request.user
        qs = user.posts_set.all()
        serializer = PostSerializer(qs, many=True)
        return Response(serializer.data)

    @action(methods=["GET"], detail=True)
    # localhost:8000/api/v2/posts/1/get_comments/
    def get_comments(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        post = Posts.objects.get(id=id)
        qs = post.comments_set.all()
        serializer = CommentModelSerializer(qs, many=True)
        return Response(serializer.data)