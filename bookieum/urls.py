from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.static import serve
from django.urls import re_path
import settings

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('kakao/', include('kakao.urls'), name='kakao'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
]
