from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.shortcuts import get_object_or_404
from bookieum import models


@csrf_exempt
@require_POST
def logout(request):
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
    
    # 로그아웃 처리
    user_list = get_object_or_404(models.Users, access_token=access_token)
    user_list.access_token = ''
    user_list.save()
    print(request.session['user_id'])
    print('user_id' in request.session)
    del request.session['user_id']
    print('user_id' in request.session)
    
    return JsonResponse({'message': 'successfully'})