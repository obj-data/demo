# -*- codeing = utf -*-
# @Time : 2022/3/1 1:42
# @Author : 陈迪曙
# @File : urls.py
# @software : PyCharm
from django.urls import path
from . import views

urlpatterns = [
    path('', views.registered, name='registered')
]