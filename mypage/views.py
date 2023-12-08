# from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from django.http.response import JsonResponse
from bookieum import models

import requests, json
import datetime as dt
from pytz import timezone

from django.core import serializers

from django.forms.models import model_to_dict

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
    
    # 코드 수정    
    
    user_list = get_object_or_404(models.Users, access_token=access_token)
    #user_list.home_addr=None
    #user_list.save()
    print(user_list)
    user_list=model_to_dict(user_list)
    print(user_list)


    # history
    user = models.Users.objects.get(access_token=access_token)
    books = models.RecommendBooks.objects.filter(user=user).select_related('isbn').exclude(is_selected=0).order_by('-created_datetime').all()
    history = []
    for book in books:
        history.append({"mybook_id": book.mybook_id, "recommend_id": book.recommend.recommend_id, "curr_page": book.curr_page, "created_datetime": book.created_datetime,
                             "is_selected": book.is_selected, "title": book.isbn.title, "cover": book.isbn.cover})
    
    return JsonResponse({'message': 'successfully', 'data':user_list,'history':history })  
 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # user_list = get_object_or_404(models.Users, access_token=access_token)
    #print(user_list)
    #return HttpResponse("ok")
    #user_list=models.Users.objects.filter(access_token=access_token)
    # user_list = get_object_or_404(models.Users, access_token=access_token)
    
    #user_list.access_token = ''
    #user_list.save()  # 모델 추가
    #return JsonResponse({'message': 'successfully', 'data': user_list})
    #return JsonResponse({'message': 'successfully', 'data': access_token})
    
    