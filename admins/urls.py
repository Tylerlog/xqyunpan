#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib import admin
from admins import views

urlpatterns = [
    url(r'^login/(.*)', views.Login.as_view(),name='login'),
    url(r"^get_yzm/$", views.get_yzm,name='get_yzm'),
    url(r"^register/$",views.register,name='register'),
]
