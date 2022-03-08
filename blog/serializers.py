# -*- codeing = utf -*-
# @Time : 2022/2/27 15:06
# @Author : 陈迪曙
# @File : serializers.py
# @software : PyCharm
from rest_framework import serializers
from .models import Blog


# 创建blog
class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('username', 'title', 'body', 'date', 'owner')


# 查看blog
class BlogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('username', 'title', 'body', 'date')


# 写一个反序列化器
class BlogObjectSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    title = serializers.CharField(max_length=32, required=True)
    body = serializers.CharField(max_length=1000)
    date = serializers.DateTimeField()
    owner = serializers.CharField()

    def create(self, validated_data):
        return Blog(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        return instance



