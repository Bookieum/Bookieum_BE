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
    
    check_user_id = get_object_or_404(models.Users, access_token=access_token)
    h_user_id=check_user_id.user_id
    
    b=models.Recommend.objects.select_related('user').filter(user_id=h_user_id)
    print(b)
    
    recommend_id_list=[]
    for i in b:
        recommend_id_list.append(i.recommend_id)
        
    c=models.RecommendBooks.objects.select_related('recommend__user').filter(recommend_id__in=recommend_id_list)
    print(c)
    c_is_selected=c.filter(is_selected=1)
    print(c_is_selected)  
    
    c_is_selected_isbn=[]
    for i in c_is_selected:
        c_is_selected_isbn.append(i.isbn_id)
    print(c_is_selected_isbn)
    
    #d=models.RecommendBooks.objects.filter(isbn_id__in=c_is_selected_isbn).prefetch_related('isbn')
    d=models.Books.objects.filter(isbn_id__in=c_is_selected_isbn)
    print(d)
    
    # fe 에서 필요한 정보 더 추가가능!
    history=[]
    for i in d:
        history.append({'isbn_id':i.isbn_id,'title':i.title,'cover':i.cover})
    print(history)
        
    """
    # history
    check_user_id = get_object_or_404(models.Users, access_token=access_token)
    h_user_id=check_user_id.user_id

    # 테스트용 Recommend, Recommend_books
    #models.Recommend.objects.create(recommend_id=201,user=check_user_id,recommend_datetime='2023-12-06 17:00:00',emotion=0.5,answer_content='안뇽')    
    
    print(check_user_id.user_name)
    
    recommend_list=models.Recommend.objects.filter(user_id=h_user_id)
    print(recommend_list)
    
    recommend_id_info=[]
    for i in range(len(recommend_list)):
        recommend_id_info.append(recommend_list[i].recommend_id)
    
    recommend_books_info=[]
    for i in recommend_id_info:
        recommend_books_check=get_object_or_404(models.RecommendBooks, recommend_id=i)
        if recommend_books_check.is_selected==1:
            recommend_books_info.append(recommend_books_check)
        
    book_info=[]
    for i in recommend_books_info:
        k=get_object_or_404(models.RecommendBooks,recommend_id=i.recommend_id)
        book_info.append(k.isbn_id)
    
    print(book_info)
    
    book_list=models.Books.objects.filter(isbn_id__in=book_info)
    print(book_list)
    
    books_list=[]
    for i in book_list:
        books_list.append(model_to_dict(i))
    
    print(books_list)
    """
    
    
    
    #return JsonResponse({'message':'successfully'})
    return JsonResponse({'message': 'successfully', 'data':user_list,'history':history })  
    #return JsonResponse({'message': 'successfully', 'data':result })  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # user_list = get_object_or_404(models.Users, access_token=access_token)
    #print(user_list)
    #return HttpResponse("ok")
    #user_list=models.Users.objects.filter(access_token=access_token)
    # user_list = get_object_or_404(models.Users, access_token=access_token)
    
    #user_list.access_token = ''
    #user_list.save()  # 모델 추가
    #return JsonResponse({'message': 'successfully', 'data': user_list})
    #return JsonResponse({'message': 'successfully', 'data': access_token})
    
    