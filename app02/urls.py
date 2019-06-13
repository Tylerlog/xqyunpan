#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib import admin
from app02 import views
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^share', views.share, name='home'),
    url(r'^upload', views.upload),
    url(r'^select_file', views.select),
    url(r'^download/(.*)', views.download,name='download_file'), # 单个文件下载
    url(r'^download_pack', views.download_pack),  # 多个文件下载
    url(r'^share_page/(.*)', views.share_page),  # 分享
    url(r'^delete', views.delete),
    url(r'^update', views.update),


    url(r'^aaa', views.aaa),

]
