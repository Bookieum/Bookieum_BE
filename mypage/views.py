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
    


@csrf_exempt
@require_POST
def book_detail(request):

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

    # 조인
    #d=models.RecommendBooks.objects.filter(isbn_id__in=RecommendbooksModel_is_selected_isbn).prefetch_related('isbn')
    #book = models.Books.objects.filter(recommend_id__in=recommend_id_list).select_related("isbn").exclude(is_selected=0)
    #books = models.RecommendBooks.objects.filter(recommend_id__in=recommend_id_list).select_related("isbn")
    #print(books)

    #books=models.Books.objects.prefetch_related('isbn_id').filter(isbn_id__in=RecommendbooksModel_is_selected_isbn)
    #print(books)

    # 세연
    """
    d = models.RecommendBooks.objects.filter(user=h_user_id).select_related('isbn').all()
    print(d)

    e = models.RecommendBooks.objects.filter(user=h_user_id).select_related('isbn').exclude(is_selected=0).order_by(
        '-created_datetime').all()
    print(e)
    """
    books = models.RecommendBooks.objects.filter(user=h_user_id).select_related('isbn').exclude(is_selected=0).order_by('-created_datetime').all()
    print(books)

    result_books = []
    for book in books:
        result_books.append({"mybook_id": book.mybook_id, "recommend_id": book.recommend_id, "curr_page": book.curr_page, "created_datetime": book.created_datetime,
                             "is_selected": book.is_selected, "title": book.isbn.title, "cover": book.isbn.cover})

    #history.append({'isbn_id':i.isbn_id,'title':i.title,'cover':i.cover})

    return JsonResponse({'message': 'successfully','result_books':result_books})


    """
    # fe 에서 필요한 정보 더 추가가능!
    detail = []
    for i in book:
        detail.append({'isbn_id': i.isbn_id, 'title': i.title, 'author': i.author, 'publisher': i.publisher,
                       'pub_date': i.pub_date,
                       'category_id': i.category_id, 'cover': i.cover, 'description': i.description,
                       'page_num': i.page_num})
    print(detail)
    # return JsonResponse({'message': 'successfully', 'detail':detail })
    """
    """
    # d=models.RecommendBooks.objects.filter(isbn_id__in=c_is_selected_isbn).prefetch_related('isbn')
    result = models.Books.objects.filter(isbn_id__in=RecommendbooksModel_is_selected_isbn)
    print(result)

    # fe 에서 필요한 정보 더 추가가능!
    detail = []
    for i in result:
        detail.append({'isbn_id': i.isbn_id, 'title': i.title, 'author': i.author, 'publisher': i.publisher,
                       'pub_date': i.pub_date,
                       'category_id': i.category_id, 'cover': i.cover, 'description': i.description,
                       'page_num': i.page_num})
    print(detail)

    return JsonResponse({'message': 'successfully', 'detail': detail})
    """