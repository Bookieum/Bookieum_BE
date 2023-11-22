from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from bookieum import models

from django.conf import settings
import requests, json
import datetime as dt
from pytz import timezone

import os

# KAKAO_CONFIG = {
#     "KAKAO_REST_API_KEY": settings.SOCIALACCOUNT_PROVIDERS['kakao']['APP']['client_id'],
#     "KAKAO_CLIENT_SECRET_KEY": settings.SOCIALACCOUNT_PROVIDERS['kakao']['APP']['secret'], 
# }

# kakao_login_uri = "https://kauth.kakao.com/oauth/authorize"
# kakao_token_uri = "https://kauth.kakao.com/oauth/token"
kakao_profile_uri = "https://kapi.kakao.com/v2/user/me"


def kakao_login(request):
    # access token 받아오기
    print(access_token)
    access_token = request.POST.get("code")
    
    # kakao 회원정보 요청
    user_info_json = request_user_info(access_token)
    
    # 회원가입 및 로그인
    social_type = 'kakao'
    social_id = f"{social_type}_{user_info_json.get('id')}"
    
    kakao_account = user_info_json.get('kakao_account')
    # 에러 처리
    # if not kakao_account:
        # return Response(status=status.HTTP_400_BAD_REQUEST)
    
    user_name = kakao_account.get('profile').get('nickname')
    gender = kakao_account.get('gender')
    
    if not models.Users.objects.filter(user_id=social_id).exists():
        user_list = models.Users()
        user_list.user_id = social_id
        user_list.user_name = user_name
        user_list.gender = gender
        user_list.reading_level = 0
        user_list.share_cnt = 0
        user_list.register_datetime = dt.datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
        user_list.save()
        request.session['user_id'] = social_id
    else:
        request.session['user_id'] = social_id 
    
    user_info = {
        'social_id': social_id,
        'user_name': user_name,
        'gender': gender,
    }
    
    return JsonResponse({'user_info': user_info})
        

# 회원 정보 요청 함수
def request_user_info(access_token):
    auth_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-type": "application/x-www-form-urlencoded",
    }
    user_info_json = requests.get(kakao_profile_uri, headers=auth_headers).json()
    
    return user_info_json