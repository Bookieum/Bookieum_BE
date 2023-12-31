from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('kakao/', include('kakao.urls')),
    path('google2/', include('google2.urls')),
    path('naver/', include('naver.urls')),
    path('logout/', include('logout.urls')),
    path('main/', include('main.urls')),
    path('mypage/',include('mypage.urls')),
    path('survey/',include('survey.urls')),
]
