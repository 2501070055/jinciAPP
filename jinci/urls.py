"""jinci URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views import static
from django.views.static import serve

from jinci import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # 用户模块
    path('v1/users/', include('users.urls')),
    # 系统模块
    path('v1/system/', include('system.urls')),
    # 板块模块
    path('v1/plates/', include('plates.urls')),
    # 评论模块
    path('v1/comments/', include('comments.urls')),
    # 邮件模块
    path('v1/emaillist/', include('emaillist.urls')),
    # md编辑器
    path(r'mdeditor/', include('mdeditor.urls')),
    # 图片上传地址
    url(r'^medias/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static'),
]
