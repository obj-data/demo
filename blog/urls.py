# -*- codeing = utf -*-
# @Time : 2022/2/27 15:05
# @Author : 陈迪曙
# @File : urls.py
# @software : PyCharm
from django.urls import path
from . import views

urlpatterns = [
    path('userblog/', views.BlogUserList.as_view(), name='blog'),
    path('detail/<title>/', views.blog_detail, name='blog_detail'),
    path('list/', views.BlogList.as_view(), name='blog_list'),
]