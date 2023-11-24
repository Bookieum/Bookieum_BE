from django.http import JsonResponse
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from bookieum import models

import requests, json
import datetime as dt
from pytz import timezone

kakao_profile_uri = "https://kapi.kakao.com/v2/user/me"

@csrf_exempt
@require_POST
def kakao_login(request):
    # data 받아오기
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError as e:
        # JSON 디코딩 중에 오류가 발생한 경우
        error_message = {'message': 'Invalid JSON format'}
        return JsonResponse(error_message, status=400)
    if not data:
        error_message = {'message': 'data을 받아오지 못했습니다.'}
        return JsonResponse(error_message, status=400)
    
    # access token 추출
    access_token = data["access_token"]
    if not access_token:
        error_message = {'message': 'access token을 받아오지 못했습니다.'}
        return JsonResponse(error_message, status=400)
    
    # kakao 회원정보 요청
    user_info_json = request_user_info(access_token)
    if not user_info_json:
        error_message = {'message': '유저 정보를 받아오지 못했습니다.'}
        return JsonResponse(error_message, status=400)
    
    # 회원가입 및 로그인
    social_type = 'kakao'
    social_id = f"{social_type}_{user_info_json.get('id')}"
    
    kakao_account = user_info_json.get('kakao_account')
    if not kakao_account:
        error_message = {'message': '카카오 계정을 받아오지 못했습니다.'}
        return JsonResponse(error_message, status=400)
    
    user_name = kakao_account.get('profile').get('nickname')
    gender = kakao_account.get('gender')
    
    if not models.Users.objects.filter(user_id=social_id).exists():
        user_list = models.Users()
        user_list.user_id = social_id
        user_list.user_name = user_name
        user_list.gender = gender
        user_list.reading_level = 0
        user_list.share_cnt = 0
        user_list.access_token = access_token
        user_list.register_datetime = dt.datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
        user_list.save()
        request.session['user_id'] = social_id
    else:
        user_list = models.Users.objects.filter(user_id=social_id)
        user_list.access_token = access_token
        user_list.save()
    
    return JsonResponse({'message': 'successfully', 'data': kakao_account})
           

# 회원 정보 요청 함수
def request_user_info(access_token):
    auth_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-type": "application/x-www-form-urlencoded",
    }
    user_info_json = requests.get(kakao_profile_uri, headers=auth_headers).json()
    
    return user_info_json