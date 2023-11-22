from django.http import JsonResponse
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from bookieum import models

import requests, json
import datetime as dt
from pytz import timezone

kakao_profile_uri = "https://kapi.kakao.com/v2/user/me"

@csrf_exempt
def kakao_login(request):
    if request.method == 'POST':
        # data 받아오기
        data = json.loads(request.body.decode('utf-8'))
        if not data:
            raise Http404("data을 받아오지 못했습니다.")
        
        # access token 추출
        access_token = data["access_token"]
        if not access_token:
            raise Http404("access token을 받아오지 못했습니다.\ndata:", data)
        
        # kakao 회원정보 요청
        user_info_json = request_user_info(access_token)
        if not user_info_json:
            raise Http404("유저 정보를 받아오지 못했습니다.")
        
        # 회원가입 및 로그인
        social_type = 'kakao'
        social_id = f"{social_type}_{user_info_json.get('id')}"
        
        kakao_account = user_info_json.get('kakao_account')
        if not kakao_account:
            raise Http404("카카오 계정을 받아오지 못했습니다.")
        
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
    # POST 요청이 아닐 경우
    else:
        raise Http404("잘못된 요청입니다. (GET 요청)")
           

# 회원 정보 요청 함수
def request_user_info(access_token):
    auth_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-type": "application/x-www-form-urlencoded",
    }
    user_info_json = requests.get(kakao_profile_uri, headers=auth_headers).json()
    
    return user_info_json