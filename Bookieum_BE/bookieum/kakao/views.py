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

KAKAO_CONFIG = {
    "KAKAO_REST_API_KEY": settings.SOCIALACCOUNT_PROVIDERS['kakao']['APP']['client_id'],
    "KAKAO_REDIRECT_URI": "http://localhost:8000/kakao/oauth",
    "KAKAO_CLIENT_SECRET_KEY": settings.SOCIALACCOUNT_PROVIDERS['kakao']['APP']['secret'], 
}

kakao_login_uri = "https://kauth.kakao.com/oauth/authorize"
kakao_token_uri = "https://kauth.kakao.com/oauth/token"
kakao_profile_uri = "https://kapi.kakao.com/v2/user/me"


def kakao_login(request):
    # 1) 코드 받아오기
    code = request.GET.get("code")
    # code 없을 경우 에러 발생
    # if not code:
    #     return Response(status=status.HTTP_400_BAD_REQUEST, data=error)
    
    # 2) access_token 요청
    access_token = request_token(code)
    # 토큰 없을 경우 에러 발생
    # if not access_token:
    #     return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # 3) kakao 회원정보 요청
    user_info_json = request_user_info(access_token) 
    
    # 4) 회원가입 및 로그인
    social_type = 'kakao'
    social_id = f"{social_type}_{user_info_json.get('id')}"
    
    kakao_account = user_info_json.get('kakao_account')
    # 에러 처리
    # if not kakao_account:
        # return Response(status=status.HTTP_400_BAD_REQUEST)
    
    user_name = kakao_account.get('profile').get('nickname')
    user_email = kakao_account.get('email')
    birth_date = kakao_account.get('birthday')
    gender = kakao_account.get('gender')
    
    if not list(models.Users.objects.filter(user_id=social_id)):
        user_list = models.Users()
        user_list.user_id = social_id
        user_list.user_name = user_name
        user_list.gender = gender
        user_list.age = 25 # 일단 임의로 넣기
        user_list.reading_level = 0
        user_list.share_cnt = 0
        user_list.register_datetime = dt.datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
        user_list.save()
        user_list.save()
        request.session['user_id'] = social_id
    else:
        request.session['user_id'] = social_id 
    
    user_info = {
        'social_type': social_type,
        'social_id': social_id,
        'user_email': user_email,
        'user_name': user_name,
        'gender': gender,
        'birth_date': birth_date
    }
        
    return redirect(f'http://localhost:3000?token={access_token}') 
 
 
# 토큰 요청 함수
def request_token(code):       
    request_data = {
        'grant_type': 'authorization_code',
        'client_id': KAKAO_CONFIG['KAKAO_REST_API_KEY'],
        'redirect_uri': KAKAO_CONFIG['KAKAO_REDIRECT_URI'],
        'client_secret': KAKAO_CONFIG['KAKAO_CLIENT_SECRET_KEY'],
        'code': code,
    }
    token_headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    access_token = requests.post(kakao_token_uri, data=request_data, headers=token_headers).json().get('access_token')
    
    return access_token


# 회원 정보 요청 함수
def request_user_info(access_token):
    auth_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-type": "application/x-www-form-urlencoded",
    }
    user_info_json = requests.get(kakao_profile_uri, headers=auth_headers).json()
    
    return user_info_json