from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from bookieum import models

import requests, json
import datetime as dt
from pytz import timezone

naver_profile_url = "https://openapi.naver.com/v1/nid/me"


@csrf_exempt
@require_POST
def naver_login(request):
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
    
    # code 추출
    code = data["code"]
    if not code:
        error_message = {'message': 'code를 받아오지 못했습니다.'}
        return JsonResponse(error_message, status=400)
    
    # access token 요청
    client_id = 'smCljzCdxfjm9Zp4EBDC'
    client_secret = 'BBU6eL7SkK'
    redirect_uri = 'http://ec2-13-124-237-120.ap-northeast-2.compute.amazonaws.com:8000/naver/oauth'

    token_req = requests.post(f"https://nid.naver.com/oauth2.0/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={redirect_uri}")
    access_token = token_req.json().get('access_token')
    
    # naver 회원정보 요청
    user_info_json = requests.get(f"{naver_profile_url}?access_token={access_token}").json()
    if not user_info_json:
        error_message = {'message': '유저 정보를 받아오지 못했습니다.'}
        return JsonResponse(error_message, status=400)
    
    # 회원가입 및 로그인
    social_type = 'naver'
    user_info = user_info_json.get('response')
    social_id = f"{social_type}_{user_info.get('id')}"
    user_name = user_info.get('name')
    gender = 'female' if user_info.get('gender') == 'F' else 'male'
    
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
        user_list = models.Users()
        user_list.access_token = access_token
        request.session['user_id'] = social_id
        
    return JsonResponse({'message': 'successfully', 'data': user_info_json, 'access_token': access_token})
    