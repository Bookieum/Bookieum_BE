from django.urls import path, include
import kakao.views as kakao_views

urlpatterns = [
    path('oauth', kakao_views.kakao_login),
]
