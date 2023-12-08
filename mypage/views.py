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
    user = models.Users.objects.get(access_token=access_token)
    books = models.RecommendBooks.objects.filter(user=user).select_related('isbn').exclude(is_selected=0).order_by('-created_datetime').all()
    history = []
    for book in books:
        history.append({"mybook_id": book.mybook_id, "recommend_id": book.recommend.recommend_id, "curr_page": book.curr_page, "created_datetime": book.created_datetime,
                             "is_selected": book.is_selected, "title": book.isbn.title, "cover": book.isbn.cover})

    return JsonResponse({'message': 'successfully', 'data':user_list,'history':history })  
    



def book_detail(request):
    mybook_id = request.GET.get("mybook")
    book = models.RecommendBooks.objects.get(mybook_id=mybook_id)
    book_info = {"mybook_id": book.mybook_id, "isbn_id": book.isbn.isbn_id, "recommend_id": book.recommend_id, "user_id": book.user.user_id,
                 "created_datetime": book.created_datetime, "curr_page": book.curr_page, "progress_rate": round(book.curr_page/book.isbn.page_num*100, 1),
                 "is_completed": book.is_completed, "title": book.isbn.title, "author": book.isbn.author, "publisher": book.isbn.publisher, 
                 "pub_date": book.isbn.pub_date, "category_name": book.isbn.category_name, "description": book.isbn.description, "cover": book.isbn.cover,
                 "page_num": book.isbn.page_num, "pos_emotion": round(float(book.recommend.emotion)*100, 2), 'neg_emotion': round((1-float(book.recommend.emotion))*100, 2),
                 "answer_content": book.recommend.answer_content}
    
    return JsonResponse({'message': 'successfully','book_info': book_info})