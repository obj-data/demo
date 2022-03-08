# -*- codeing = utf -*-
# @Time : 2022/3/1 1:12
# @Author : 陈迪曙
# @File : serializers.py
# @software : PyCharm
from django.contrib.auth import get_user_model  # 获取活动中的user表
from rest_framework import serializers

User = get_user_model()  # 实例化用户表


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True, required=True, style={"input_type": "password"},
                                      label="Confirm password")  # 确认密码

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):  # 重写创建函数
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        password2 = validated_data['password2']
        if email and User.objects.filter(email=email).exclude(username=username).exists():  # 防止邮箱重复
            raise serializers.ValidationError({'email': '邮箱不允许重复'})
        if password2 != password:
            raise serializers.ValidationError({'password': '两次输入的密码不一致'})
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return user
