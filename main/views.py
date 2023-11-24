# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_POST
# from bookieum import models
# from django.core.files.storage import FileSystemStorage  # 파일저장


# @csrf_exempt
# @require_POST
# def recommendation(request):
#     # 1) 데이터 받아오기
#     video = request.FILES['video']
#     fs = FileSystemStorage()
#     video_name = fs.save("video.mp3", video)
    
#     # 2) AI 책 추천
#     # book_list = recommend_ai_logic(받아온 데이터 넣기)
    
#     # 3) 추천 책 정보 조회
    
#     # 4) 추천 내역 및 도서 리스트 DB에 저장
    
#     return JsonResponse({'message': 'successfully', 'data': '[책 정보들 리스트]'})


# # AI 로직
# # def recommend_ai_logic():
#     # 요청 1. 측정한 감정값을 리턴해주세요! (emotion)
#     # 요청 2. 추천 책들을 리스트로 리턴하게 짜주세요! (book_list)
#         # [{'isbn_id': .., 'title': .., ...}, {'isbn_id': .., 'title': .., ...}] 이렇게 가능하면 더 좋구요!
#         # 안되면 [아이디, 아이디, 아이디] 이렇게 짜주세요!
#     # return emotion, book_list