# from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from bookieum import models

import requests, json
import datetime as dt
from pytz import timezone

from django.core import serializers

@csrf_exempt
@require_POST
def survey_page(request):
    """
    # data 받아오기 (설문1)
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

    
    if models.Users.objects.filter(access_token=access_token).exists():
        user_list = get_object_or_404(models.Users, access_token=access_token)
        if user_list.survey=="False":
            genredata=data
            user_list.genre=genredata
            user_list.save()
    
              
    """

    """    
    # data 받아오기 (설문2)
    try:
        data1 = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError as e:
        # JSON 디코딩 중에 오류가 발생한 경우
        error_message = {'message': 'Invalid JSON format'}
        return JsonResponse(error_message, status=400)
    if not data1:
        error_message = {'message': 'data을 받아오지 못했습니다.'}
        return JsonResponse(error_message, status=400)
    
    # access token 추출
    access_token1 = data1["access_token"]
    if not access_token1:
        error_message = {'message': 'access token을 받아오지 못했습니다.'}
        return JsonResponse(error_message, status=400)    
    
    if models.Users.objects.filter(access_token=access_token1).exists():
        user_list1 = get_object_or_404(models.Users, access_token=access_token1)
        if user_list1.survey=="False":
            mooddata=data
            user_list1.mood=mooddata
            user_list1.save()
            
    """  

    """
    # data 받아오기 (설문3)
    try:
        data2 = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError as e:
        # JSON 디코딩 중에 오류가 발생한 경우
        error_message = {'message': 'Invalid JSON format'}
        return JsonResponse(error_message, status=400)
    if not data2:
        error_message = {'message': 'data을 받아오지 못했습니다.'}
        return JsonResponse(error_message, status=400)
    
    # access token 추출
    access_token2 = data2["access_token"]
    if not access_token2:
        error_message = {'message': 'access token을 받아오지 못했습니다.'}
        return JsonResponse(error_message, status=400)    
    
    user_list = get_object_or_404(models.Users, access_token=access_token2)
    if user_list.survey=="False":
        interest=data2['survey']
        user_list.interest=interest
        #user_list.save()
        user_list.save()
    """
    
    # return JsonResponse({'message': 'successfully'})
    
    
    # data 받아오기 (설문1)
    try:
        data = json.loads(request.body.decode('utf-8'))
        print(data)
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
    
    # 한번에 json 오는것.
    type = data['type']
    user_list = get_object_or_404(models.Users, access_token=access_token)
    user_list.survey='False'
    # user_list=models.Users.objects.filter(access_token=access_token)
    if user_list.survey=="False":
        if type == 'genre':
            user_list.genre = data['survey'] 
        
        elif type=='mood':
            user_list.mood=data['survey']

        else:
            user_list.interest=data['survey']
            user_list.survey="True"
    
    
        user_list.save()
                
        return JsonResponse({'message': 'successfully'})
        
        
        
    
  
        
        
        
