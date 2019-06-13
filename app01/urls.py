#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib import admin
from app01 import views
urlpatterns = [
    url(r'^$', views.login),
    url(r'^login/verify', views.verify),
    url(r'^login/random', views.random),
    url(r'^login/accredit', views.accredit),
    url(r'^login', views.login,name='head'),
    url(r'^aaa', views.aaa),

]
