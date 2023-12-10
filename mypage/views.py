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
    user_info = model_to_dict(get_object_or_404(models.Users, access_token=access_token))
    # 읽은 권수 및 레벨업에 필요한 권수
    user = models.Users.objects.get(access_token=access_token)
    complete_book = models.RecommendBooks.objects.filter(user=user, is_completed=1).all()
    reading_num = len(complete_book)
    user_info['reading_num'] = reading_num
    # 0~9 권: 0레벨 / 10~49권: 1레벨 / 50~99권: 2레벨 / 100권 이상: 3레벨 
    if user_info['reading_level'] == 0:
        user_info['need_num'] = 10 - reading_num
    elif user_info['reading_level'] == 1:
        user_info['need_num'] = 50 - reading_num
    elif user_info['reading_level'] == 2:
        user_info['need_num'] = 100 - reading_num
    else:
        user_info['need_num'] = 0

    # history
    books = models.RecommendBooks.objects.filter(user=user).select_related('isbn').exclude(is_selected=0).order_by('-created_datetime').all()
    history = []
    for book in books:
        history.append({"mybook_id": book.mybook_id, "recommend_id": book.recommend.recommend_id, "curr_page": book.curr_page, "created_datetime": book.created_datetime,
                             "is_selected": book.is_selected, "title": book.isbn.title, "cover": book.isbn.cover})

    return JsonResponse({'message': 'successfully', 'data':user_info,'history':history })  
    

# 책 상세 페이지
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


# 진도 관리
@csrf_exempt
@require_POST
def book_progress(request):
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
    if access_token == "":
        error_message = {'message': 'access token이 비어있습니다. (로그인 상태가 아닙니다.)'}
        return JsonResponse(error_message, status=400)
    user = models.Users.objects.get(access_token=access_token)
    
    # mybook_id 추출
    mybook_id = data["mybook_id"]
    if not mybook_id:
        error_message = {'message': 'mybook_id를 받아오지 못했습니다.'}
        return JsonResponse(error_message, status=400)
    
    # curr_page 추출
    curr_page = data["curr_page"]
    if not curr_page:
        error_message = {'message': 'curr_page를 받아오지 못했습니다.'}
        return JsonResponse(error_message, status=400) 
    
    # DB 반영 및 에러처리
    recommend_book = models.RecommendBooks.objects.get(mybook_id=mybook_id)
    if int(curr_page) > recommend_book.isbn.page_num:
        error_message = {'message': 'curr_page는 page_num을 초과할 수 없습니다.'}
        return JsonResponse(error_message, status=400)
    if int(curr_page) < 0:
        error_message = {'message': 'curr_page는 0보다 작을 수 없습니다.'}
        return JsonResponse(error_message, status=400)
    if recommend_book.user != user:
        error_message = {'message': '로그인한 사용자와 mybook 내역의 사용자가 다릅니다. (잘못된 시도입니다.)'}
        return JsonResponse(error_message, status=400)
    recommend_book.curr_page = curr_page
    # 다 읽었으면 is_completed 1로 변경 + 독서레벨 계산 및 반영
    if int(curr_page) == recommend_book.isbn.page_num:
        recommend_book.is_completed = 1
        # 독서레벨 계산 및 반영
        # 0~9 권: 0레벨 / 10~49권: 1레벨 / 50~99권: 2레벨 / 100권 이상: 3레벨 
        complete_book = models.RecommendBooks.objects.filter(user=user, is_completed=1).all()
        num = len(complete_book)+1 # 방금 더한 1은 반영이 안되었으므로 더해준다.
        print(num)
        if num >= 100:
            user.reading_level = 3
        elif num >= 50:
            user.reading_level = 2
        elif num >= 10:
            user.reading_level = 1
        else:
            user.reading_level = 0
        user.save()
    recommend_book.save()
    
    
    
    return JsonResponse({'message': 'successfully','mybook_id': mybook_id})