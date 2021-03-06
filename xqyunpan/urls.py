"""xqyunpan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from app01 import views
from app02 import views as app01_views
# from admins import urls as admins_urls
urlpatterns = [
    url(r"^admins/",include('admins.urls')),
    url(r'^home/', include('app02.urls')),
    url(r'^title', app01_views.title),

    url(r'^', views.error),
    url(r'^admin/', admin.site.urls),
]
