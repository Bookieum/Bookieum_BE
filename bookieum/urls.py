from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('kakao/', include('kakao.urls')),
    path('google/', include('google.urls')),
]
