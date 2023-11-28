from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from bookieum import models
from django.core.files.storage import FileSystemStorage  # 파일저장
import json


@csrf_exempt
@require_POST
def recommendation(request):
    # 1) 데이터 불러오기
    # 비디오 저장
    uploaded_file = request.FILES['video']
    file_name = uploaded_file.name
    fs = FileSystemStorage()
    fs.save(file_name, uploaded_file)
    # 텍스트 불러오기
    text = request.POST.get('text', '')
                         
    # 2) AI 책 추천
    emotion, book_list = recommend_ai_logic('/media/'+file_name, text)
    
    # 3) 추천 책 정보 조회
    
    # 4) 추천 내역 및 추천 도서 리스트 DB에 저장
    
    # return JsonResponse({'message': 'successfully', 'data': '[책 정보들 리스트]'})
    return JsonResponse({'message': 'successfully', 'data': {'text': text}})
 


# AI 로직
def recommend_ai_logic(file_path, text):
    # 영상 관련
        # 루트 경로에 media 폴더 생성해야 함
        # file_path는 영상 경로 ('/media/파일명')
        # 영상 사용 후에 영상 삭제하는 코드 넣어주세요!
    # 요청 1. 측정한 감정값을 리턴해주세요! (emotion)
    # 요청 2. 추천 책들을 리스트로 리턴하게 짜주세요! (book_list)
        # [{'isbn_id': .., 'title': .., ...}, {'isbn_id': .., 'title': .., ...}] 이렇게 가능하면 더 좋구요!
        # 안되면 [아이디, 아이디, 아이디] 이렇게 짜주세요!
    # return emotion, book_list
    return 0.56, [] # 이건 지우면 됨!
