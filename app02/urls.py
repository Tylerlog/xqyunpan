#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib import admin
from app02 import views
urlpatterns = [
    url(r'^$', views.home),
    url(r'^all', views.all), # 所有文件
    url(r'^pic', views.pic), # 图片文件
    url(r'^doc', views.doc), # 文档文件
    url(r'^video', views.video), # 视频文件
    url(r'^music', views.music), # 音乐文件
    url(r'^rests', views.rests), # 其他文件
    url(r'^share/', views.share),
    url(r'^upload', views.upload),
    url(r'^select_file', views.select),
    url(r'^download/(.*)', views.download,name='download_file'), # 单个文件下载
    url(r'^download_pack', views.download_pack),  # 多个文件下载
    url(r'^share_page/(.*)', views.share_page),  # 生成分享
    url(r'^share_list', views.share_list),  # 分享列表
    url(r'^share_link/(.*)', views.share_link),  # 分享列表
    url(r'^share_cancel', views.share_cancel),  # 分享网址
    url(r'^select_share_link/(.*)', views.select_share_link),  # 分享下载列表
    url(r'^delete', views.delete),
    url(r'^update', views.update),


    url(r'^aaa', views.aaa),

]
