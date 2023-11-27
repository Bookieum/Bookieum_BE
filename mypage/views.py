# from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from bookieum import models

import requests, json
import datetime as dt
from pytz import timezone

from django.core import serializers

@csrf_exempt
@require_POST
def user_information(request):
    
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
    

    
    # 마이페이지 로그인 정보 (세션)
    
    # user_id = request.session.get('user_id')
    
    # 세션없이 user_information 부분 구현.
    
    """
    user_list = get_object_or_404(models.Users, access_token=access_token)
    user_list=json.dumps(list(user_list))
    return JsonResponse({'message': 'successfully', 'data': user_list})
    """
    
    """
    # 모든 객체 반환
    user_list=models.Users.objects.filter(access_token=access_token)
    user_list=serializers.serialize('json',user_list)
    return JsonResponse({'message': 'successfully', 'data': user_list})
    """
  
    user_list=models.Users.objects.filter(access_token=access_token)
    user_list=serializers.serialize('json',user_list)
    return JsonResponse({'message': 'successfully', 'data':user_list})  
    
    # user_list = get_object_or_404(models.Users, access_token=access_token)
    #print(user_list)
    #return HttpResponse("ok")
    #user_list=models.Users.objects.filter(access_token=access_token)
    # user_list = get_object_or_404(models.Users, access_token=access_token)
    
    #user_list.access_token = ''
    #user_list.save()  # 모델 추가
    #return JsonResponse({'message': 'successfully', 'data': user_list})
    #return JsonResponse({'message': 'successfully', 'data': access_token})