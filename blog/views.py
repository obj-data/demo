import json

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, generics
from .serializers import BlogSerializer, BlogListSerializer, BlogObjectSerializer
from .models import Blog
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, AllowAny
from .authJWT import AuthToken

# Create your views here.

def test_user(request):
    request.data['owner'] = User._get_pk_val(request.user)
    request.data['username'] = User.get_username(request.user)
    serializer = BlogSerializer(data=request.data)
    return serializer


class BlogUserList(generics.ListAPIView):
    authentication_classes = [AuthToken]
    '''
    get: 获取用户自己的所有博客(需登录)

    post: 新建博客(需登录)
    '''

    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def post(self, request):
        serializer = None
        if test_user(request):
            serializer = test_user(request=request)
        else:
            return Response('只能修改自己创建的博客', status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response(True, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        username = self.request.user.get_username()
        data = Blog.objects.filter(username=username).values('username', 'title', 'body', 'date')
        return Response(data)


class BlogList(generics.ListAPIView, ):
    '''
    (无需登录)
    get: 获取所有blog
    post: 废弃
    '''
    queryset = Blog.objects.values('username', 'title', 'body', 'date')
    serializer_class = BlogListSerializer

    def post(self, request):
        raise Http404


# 修改个人博客，覆盖式修改(未完成)
@api_view(['PUT', 'DELETE'])
def blog_detail(request, title):
    request.user = AuthToken().authenticate(request)[0]
    '''
    修改或删除博客(需登录)
    '''
    try:
        blog = Blog.objects.get(title=title)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = None
        if test_user(request):
            serializer = test_user(request=request)
        else:
            return Response('只能修改自己创建的博客', status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            blog.title = serializer.data['title']
            blog.body = serializer.data['body']
            blog.save()
            return Response('修改成功', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        if request.user.get_username() == blog.username:
            blog.delete()
            return Response('删除博客成功!', status=status.HTTP_204_NO_CONTENT)
        return Response('你无权删除此博客', status=status.HTTP_400_BAD_REQUEST)



