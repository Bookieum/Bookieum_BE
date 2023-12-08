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
    
    # user_information
    user_list = get_object_or_404(models.Users, access_token=access_token)
    #user_list.home_addr=None
    #user_list.save()
    print(user_list)
    user_list=model_to_dict(user_list)
    print(user_list)

    # history
    check_user_id = get_object_or_404(models.Users, access_token=access_token)
    h_user_id=check_user_id.user_id
    
    # 조인
    RecommendModel=models.Recommend.objects.select_related('user').filter(user_id=h_user_id)
    print(RecommendModel)
    
    recommend_id_list=[]
    for i in RecommendModel:
        recommend_id_list.append(i.recommend_id)
     
    # 조인   
    RecommendbooksModel=models.RecommendBooks.objects.select_related('recommend__user').filter(recommend_id__in=recommend_id_list)
    print(RecommendbooksModel)
    RecommendbooksModel_is_selected=RecommendbooksModel.filter(is_selected=1)
    print(RecommendbooksModel_is_selected)  
    
    RecommendbooksModel_is_selected_isbn=[]
    for i in RecommendbooksModel_is_selected:
        RecommendbooksModel_is_selected_isbn.append(i.isbn_id)
    print(RecommendbooksModel_is_selected_isbn)
    
    
    #d=models.RecommendBooks.objects.filter(isbn_id__in=c_is_selected_isbn).prefetch_related('isbn')
    result=models.Books.objects.filter(isbn_id__in=RecommendbooksModel_is_selected_isbn)
    print(result)
    
    # fe 에서 필요한 정보 더 추가가능!
    history=[]
    for i in result:
        history.append({'isbn_id':i.isbn_id,'title':i.title,'cover':i.cover})
    print(history)
    
    return JsonResponse({'message': 'successfully', 'data':user_list, 'history': history})

    