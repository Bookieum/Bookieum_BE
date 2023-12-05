from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from bookieum import models
from django.core.files.storage import FileSystemStorage  # 파일저장
import json
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
#AI
#pip install konlpy pandas seaborn gensim wordcloud python-mecab-ko wget svgling joblib requests numpy  scikit-learn opencv-python keras tensorflow


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
    text = '오늘 기분 좋아'
    request.POST.get('text', '')
    # 유저 정보 불러오기
    access_token = request.POST.get('access_token', '')
    if models.Users.objects.filter(access_token=access_token).exists():
        user = models.Users.objects.get(access_token=access_token)
    else:
        return JsonResponse({'message': 'Not Found User'})
                         
    # 2) AI 책 추천
    emotion, book_list = recommend_ai_logic('/media/'+file_name, text)

    # 3) 추천 내역 및 추천 도서 리스트 DB에 저장
    recommend_list = models.Books.objects.filter(isbn_id__in=book_list)
    recommend_books = []
    
    if recommend_list.exists():
        # Recommend
        recommend = models.Recommend.objects.create(
            user = user,
            emotion = emotion,
            answer_content = text
        )
        recommend_info = {'recommend_id': recommend.recommend_id, 'pos_emotion': emotion*100, 'neg_emotion': round((1-emotion)*100, 1)}
        
        # Recommend_books
        for rec in recommend_list:
            mybook = models.RecommendBooks.objects.create(
                isbn = models.Books.objects.get(isbn_id=rec.isbn_id),
                recommend = recommend,
                user = user
            )
            
            recommend_books.append({'mybook_id': mybook.mybook_id, 'isbn_id': rec.isbn_id, 'title': rec.title, 'author': rec.author,
                                    'publisher': rec.publisher, 'pub_date': rec.pub_date, 'category_name': rec.category_name, 
                                    'cover': rec.cover, 'description': rec.description, 'page_num': rec.page_num})
            
    else:
        return JsonResponse({'message': 'Not Found Recommend Books'})
    
    
    return JsonResponse({'message': 'successfully', 'data': {'recommend_info': recommend_info, 'recommend_books': recommend_books}})
 

# AI 로직
def recommend_ai_logic(file_path, text):
    
    import tensorflow as tf
    tf.config.experimental.list_physical_devices('GPU')
    
    import joblib
    import requests
    import json
    import numpy as np
    import pandas as pd
    import warnings
    warnings.filterwarnings(action = 'ignore')
    from mecab import MeCab
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity, linear_kernel
    import cv2
    from keras.models import load_model
    import threading
    from multiprocessing import Queue
    import time
    # 영상 관련
        # 루트 경로에 media 폴더 생성해야 함
        # file_path는 영상 경로 ('/media/파일명')
        # 영상 사용 후에 영상 삭제하는 코드 넣어주세요!
        
        
    # 요청 1. 측정한 감정값을 리턴해주세요! (emotion)
    
    
    ###################################################################
   # 텍스트 감정 분석 코드
    def analyze_sentiment(sentence, client_id, client_secret):
        url = "https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"
        headers = {
            "X-NCP-APIGW-API-KEY-ID": client_id,
            "X-NCP-APIGW-API-KEY": client_secret,
            "Content-Type": "application/json"
        }

        data = {
            "content": sentence
        }

        response = requests.post(url, data=json.dumps(data), headers=headers)
        rescode = response.status_code

        if rescode == 200:
            result = json.loads(response.text)
            document = result.get("document")
            if document:
                sentiment = document.get("sentiment")
                confidence = document.get("confidence")
                if sentiment and confidence:
                    confidence_neutral = confidence.get("neutral") / 100.0 / 2.0
                    confidence_positive = confidence.get("positive") / 100.0 + confidence_neutral
                    confidence_negative = confidence.get("negative") / 100.0 + confidence_neutral

                    text_sentiment_score = confidence_positive * 0.7 + confidence_negative * 0.3

                    return {
                        "Sentiment": sentiment,
                        "Positive Confidence": round(confidence_positive, 7),
                        "Negative Confidence": round(confidence_negative, 7),
                        "Text Sentiment Score": round(text_sentiment_score, 3)
                    }
                else:
                    return {"error": "Sentiment and Confidence information not found"}
            else:
                return {"error": "Document information not found"}
        else:
            return {"error": "HTTP Error: " + response.text}


    # 얼굴 감정 분석 코드
    # def load_emotion_model(model_path):
    #     return load_model(model_path)


    def detect_emotions(video_capture, emotion_model, face_classifier):
        emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
        emotion_counts = {label: 0 for label in emotion_labels}

        start_time = time.time()
        analysis_interval = 4  # Analyze frames every 4 seconds

        while True:
            ret, frame = video_capture.read()

            if not ret:
                break

            current_time = time.time()

            if current_time - start_time >= analysis_interval:
                start_time = current_time

                labels = []
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray)

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                    roi_gray = gray[y:y + h, x:x + w]
                    roi_gray = cv2.resize(roi_gray, (224, 224), interpolation=cv2.INTER_AREA)
                    roi = cv2.cvtColor(roi_gray, cv2.COLOR_GRAY2RGB)
                    roi = roi.astype('float') / 255.0
                    roi = np.expand_dims(roi, axis=0)

                    prediction = emotion_model.predict(roi, verbose=0)[0]
                    label = emotion_labels[prediction.argmax()]
                    label_position = (x, y)
                    cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    emotion_counts[label] += 1

                #cv2.imshow('Emotion Detector', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("No more frames. Exiting loop.")
                break

        video_capture.release()
        cv2.destroyAllWindows()

        return emotion_counts


    def calculate_emotion_scores(emotion_counts):
        positive_emotions = ['Happy', 'Neutral', 'Surprise']
        negative_emotions = ['Angry', 'Disgust', 'Fear', 'Sad']

        positive_score = sum(emotion_counts[label] for label in positive_emotions)
        negative_score = sum(emotion_counts[label] for label in negative_emotions)

        total_emotions = sum(emotion_counts.values())
        positive_normalized = round(positive_score / total_emotions, 7)
        negative_normalized = round(negative_score / total_emotions, 7)
        face_sentiment_score = round(positive_normalized * 0.7 + negative_normalized * 0.3, 3)
        return positive_normalized, negative_normalized, face_sentiment_score


    def face_analysis_thread(video_capture, emotion_model,face_classifier,result_queue):
        emotion_counts = detect_emotions(video_capture, emotion_model, face_classifier)
        positive_score, negative_score, face_sentiment_score = calculate_emotion_scores(emotion_counts)
        # print(f"Face Analysis - Positive Score: {positive_score:.3f}")
        # print(f"Face Analysis - Negative Score: {negative_score:.3f}")
        #print(f"Face Analysis - Face Sentiment Score: {face_sentiment_score:.3f}")
        result_queue.put({"face_sentiment_score": face_sentiment_score})


    def text_analysis_thread(text, result_queue):
        client_id = "hpgzp4aq0t"
        client_secret = "frhqiMUgx0HT3j7AtF9fJ9h3w3hqm2w9bX7YRjK5"
        sentence = text
        result = analyze_sentiment(sentence, client_id, client_secret)
        #print("Text Analysis - Results:")
        #print(json.dumps(result, indent=4, sort_keys=True))
        result_queue.put({"text_sentiment_score": result["Text Sentiment Score"]})

    def main(text):
        # Load face classifier and emotion model
        face_classifier = cv2.CascadeClassifier(r"ai/haarcascade_frontalface_default.xml")
        # emotion_model = load_emotion_model(r"ai/Emotion_Detection.h5")

        # 비디오 파일 저장 후 경로 설정 해줘야함!!!!!!!!
        video_path = r"ai/test.mp4"
        cap = cv2.VideoCapture(video_path)
        result_queue = Queue()
        # Create threads for face analysis and text analysis
        # face_thread = threading.Thread(target=face_analysis_thread, args=(cap, emotion_model,face_classifier,result_queue))
        text_thread = threading.Thread(target=text_analysis_thread, args=(text,result_queue))

        # Start both threads
        # face_thread.start()
        text_thread.start()

        # Wait for both threads to finish
        # face_thread.join()
        text_thread.join()

        # Release video capture
        cap.release()
        cv2.destroyAllWindows()

        # Retrieve results from the Queue
        results = {"face_sentiment_score": None, "text_sentiment_score": None}
        while not result_queue.empty():
            result = result_queue.get()
            results.update(result)

        # Calculate average sentiment scores
        average_sentiment = results["text_sentiment_score"]
        # average_sentiment = (results["face_sentiment_score"] + results["text_sentiment_score"])/2.0

        # Print the results
        print(f"Average Sentiment Score: {average_sentiment:.3f}")
        return average_sentiment

    emotion_result= main(text)
    #####################################################################################
    # 요청 2. 추천 책들을 리스트로 리턴하게 짜주세요! (book_list)
    
    data = joblib.load(r'ai/data.pkl')
    collaborative_df = joblib.load(r'ai/collaborative_data.pkl')
    content_df = joblib.load(r'ai/cosine_data.pkl')

    
    # KoNLPy의 Mecab 형태소 분석기 객체 생성
    mecab = MeCab()

    # TF-IDF 벡터화를 위한 객체 생성 및 변환 완료
    book_tfidf = TfidfVectorizer()
    book_matrix = book_tfidf.fit_transform(content_df['text'])
    # 코사인 유사도 계산
    book_similarity = linear_kernel(book_matrix, book_matrix)

    # TF-IDF 벡터화를 위한 객체 생성 및 변환 완료
    feature_tfidf = TfidfVectorizer()
    feature_matrix = feature_tfidf.fit_transform(content_df['features'])
    # 코사인 유사도 계산
    feature_similarity = cosine_similarity(feature_matrix, feature_matrix)
    
    def update_data_and_cosine_sim(new_data, tfidf):
        global book_matrix, book_similarity, feature_matrix, feature_similarity

        # 원본 데이터 업데이트
        tmp = new_data.copy()

        # Content-based-filtering을 위한 하나의 문자열로 만들기
        tmp['text'] = tmp['Keyword'].apply(lambda x: ' '.join(x))
        tmp['features'] = tmp['genres'].apply(lambda x: ' '.join(x)) + ' ' + tmp['mood'].apply(lambda x: ' '.join(x)) + ' ' + tmp['interest'].apply(lambda x: ' '.join(x))

        df = tmp.copy()
        df = tmp.drop(['categoryName', 'description', 'Keyword', 'genres', 'mood', 'interest'], axis = 1)

        # TF-IDF 벡터화 객체에 새로운 데이터 적용 및 변환 완료
        book_matrix = book_tfidf.fit_transform(df['text'])  # 'content'는 실제 텍스트 컬럼명에 맞게 변경해야 합니다.
        # cosine similarity matrix 업데이트
        book_similarity = cosine_similarity(book_matrix)

        # TF-IDF 벡터화
        feature_matrix = feature_tfidf.fit_transform(df['features'])
        # 코사인 유사도 계산
        feature_similarity = cosine_similarity(feature_matrix, feature_matrix)

        return df

    # 사용자가 입력한 문장에 대한 책 추천 10권

    def recommend_books_based_on_sentence(sentence, user_read):
        # 사용자가 입력한 문장 맞춤법 검사
        # sentence = spell_checker.check(sentence).checked

        # 사용자가 입력한 문장 (형태소로 분리)
        user_input_sentence = [" ".join(mecab.morphs(sentence))]

        # 이 문장도 TF-IDF 벡터화를 수행합니다.
        user_input_tfidf = book_tfidf.transform(user_input_sentence)

        # 코사인 유사도 계산
        book_similarity_user_input = cosine_similarity(user_input_tfidf, book_matrix)

        # 가장 유사한 책들의 인덱스 찾기
        similar_book_indexes = np.argsort(-book_similarity_user_input.flatten())

        # 사용자가 이미 읽은 책 제외
        similar_book_indexes = [idx for idx in similar_book_indexes if content_df['isbn_id'].iloc[idx] not in user_read]

        # 가장 유사한 10개의 문서 인덱스 가져오기
        top_10_indexes = similar_book_indexes[:10]

        # 원본 데이터프레임에서 해당하는 행 가져오기 (여기서는 'isbn_id' 컬럼만 가져옵니다.)
        similar_books_based_on_user_input = content_df['isbn_id'].iloc[top_10_indexes]

        return similar_books_based_on_user_input.tolist()   # list 형태로 반환


    def get_book_titles_by_isbn(isbn_list):
        # isbn_list에 있는 각 isbn에 대응하는 제목 찾기
        book_titles = [content_df[content_df['isbn_id'] == isbn]['title'].values[0] for isbn in isbn_list]

        return book_titles

    def recommend_books_based_on_book(isbn, user_read, num_books=10):
        # 입력된 isbn에 해당하는 책의 인덱스 찾기
        idx = content_df[content_df['isbn_id'] == isbn].index[0]

        # 모든 책과의 cosine similarity 값 가져오기
        book_similarity_values = book_similarity[idx]

        # 가장 유사한 책들의 인덱스 찾기
        similar_book_indexes = np.argsort(-book_similarity_values)

        # 사용자가 이미 읽은 책 제외
        similar_book_indexes = [idx for idx in similar_book_indexes if content_df['isbn_id'].iloc[idx] not in user_read]

        # 가장 유사한 num_books개의 문서 인덱스 가져오기
        top_indexes = similar_book_indexes[:num_books]

        # 원본 데이터프레임에서 해당하는 행 가져오기 (여기서는 'isbn_id' 컬럼만 가져옵니다.)
        similar_books_based_on_book = content_df['isbn_id'].iloc[top_indexes]

        return similar_books_based_on_book.tolist()   # list 형태로 반환

    # genres, mood, interest로 책 추천

    def user_features_recommended_books(genres, mood, interest, user_read):
        # 사용자 features의 입력을 문자열로 합치기
        user_input = ' '.join(genres) + ' ' + ' '.join(mood) + ' ' + ' '.join(interest)

        # 사용자의 입력을 벡터화하기
        user_input_vector = feature_tfidf.transform([user_input])

        # 모든 책에 대한 사용자의 입력과의 유사도를 계산하기
        user_feature_book_similarity = linear_kernel(feature_matrix, user_input_vector)

        # 유사도에 따라 책들을 정렬하기
        sorted_similarity_scores = list(enumerate(user_feature_book_similarity))
        sorted_similarity_scores = sorted(sorted_similarity_scores, key=lambda x: x[1], reverse=True)

        # 사용자가 이미 읽은 책 제외
        sorted_similarity_scores = [score for score in sorted_similarity_scores if content_df['isbn_id'].iloc[score[0]] not in user_read]

        # 가장 유사한 10개의 책의 인덱스를 가져오기
        top10_similar_books = sorted_similarity_scores[0:10]

        # 가장 유사한 10개의 책의 인덱스를 이용하여 책의 'isbn_id'를 반환
        book_indices = [i[0] for i in top10_similar_books]
        return content_df['isbn_id'].iloc[book_indices].tolist()   # list 형태로 반환

    # collaborative filtering

    import pandas as pd
    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity

    user_book_rating = collaborative_df.pivot_table(index='nickname', columns='isbn_id', values='rating').fillna(0)

    # 코사인 유사도 계산
    user_similarity = cosine_similarity(user_book_rating)
    user_similarity_df = pd.DataFrame(user_similarity, index=user_book_rating.index, columns=user_book_rating.index)

    def get_user_recommendations(target_user):
        similar_users = user_similarity_df[target_user]

        # 유사도 순으로 정렬
        similar_users = similar_users.sort_values(ascending=False)

        # 타겟 사용자의 평점을 가져옴
        user1_ratings = user_book_rating.loc[target_user, :]

        # 가장 유사한 사용자의 리스트를 순회
        for user in similar_users.index[1:6]:
            # 각 사용자의 평점을 가져옴
            user2_ratings = user_book_rating.loc[user, :]

            # 타겟 사용자가 평가하지 않은 책 중, 평점이 3 이상인 책만 추천
            recommendations = user2_ratings[(user1_ratings == 0) & (user2_ratings >= 3)]

            # 만약 추천할 책이 있다면 반환
            if not recommendations.empty:
                # Series를 list로 변환, 평점을 제외하고 책의 ID만 반환
                return [item[0] for item in recommendations.sort_values(ascending=False).items()][:10]

        # 모든 사용자를 순회했음에도 추천할 책이 없다면 빈 리스트 반환
        return []

    # 아래내용부터 입력 들어가서 위 함수들로 책 추천 받는 로직(5권 이전일때 추천, 5권이상일때 추천)
    
    user_name = '글월마야'
    emotion = emotion_result
    sentence = text
    user_read = ['9772799628000', '9791198375308']  # 사용자가 읽었던 책 isbn13

    # 사용자의 선호장르
    genres = ['시대', '전쟁', '과학']
    mood = ['열정', '도전']
    interest = ['영화', '생각', '성공', '심리', '동물', '시간', '사진', '여행', '인간', '시', '그림', '미술']

    # 사용자 리뷰 데이터 5권 전

    def recommend_books_under_five_reviews(sentence, user_read, emotion):
        # 문장에 대해 컨텐츠 기반 필터링
        isbn_list_by_sentence = recommend_books_based_on_sentence(sentence, user_read)
        # 선호장르 기반 책 추천
        isbn_list_by_feature = user_features_recommended_books(genres, mood, interest, user_read)

        # 두 리스트를 합치고 중복 제거
        isbn_list = list(set(isbn_list_by_sentence + isbn_list_by_feature))

        # 각 isbn에 대한 감성 점수의 차이 계산
        isbn_with_emotion_diff = [(isbn, abs(data.loc[data['isbn_id'] == isbn, 'emotion_score'].values[0] - emotion)) for isbn in isbn_list]

        # 감성 점수의 차이가 최소인 순서로 정렬
        isbn_with_emotion_diff_sorted = sorted(isbn_with_emotion_diff, key=lambda x: x[1])

        # 차이가 가장 적은 상위 3권의 isbn 반환
        return [isbn for isbn, diff in isbn_with_emotion_diff_sorted[:3]]
    book_list_under_five=recommend_books_under_five_reviews(sentence, user_read, emotion)
    print(book_list_under_five)

    # 사용지 리뷰 데이터 5권 이상

    # 사용자가 읽었던 책 중 가장 평점이 높은 책
    user_prefer_isbn = '9791198173898'

    def recommend_books_over_five_reviews(sentence, user_name, user_read, user_prefer_isbn, emotion):
        # 문장에 대해 컨텐츠 기반 필터링
        isbn_list_by_sentence = recommend_books_based_on_sentence(sentence, user_read)

        # 사용자 리뷰 데이터 기반 책 추천
        isbn_list_by_review = get_user_recommendations(user_name)

        # isbn_list_by_review이 10권 이하라면,
        # 사용자 선호 도서 기반 책 추천을 통해 10권이 되도록 책 리스트를 추가
        if len(isbn_list_by_review) < 10:
            more_isbn = 10 - len(isbn_list_by_review)
            isbn_list_by_book = recommend_books_based_on_book(user_prefer_isbn, user_read, more_isbn)
        else:
            isbn_list_by_book = []

        # 세 리스트를 합치고 중복 제거
        isbn_list = list(set(isbn_list_by_sentence + isbn_list_by_review + isbn_list_by_book))

        # 각 isbn에 대한 감성 점수의 차이 계산
        isbn_with_emotion_diff = [(isbn, abs(data[data['isbn_id'] == isbn]['emotion_score'].values[0] - emotion)) for isbn in isbn_list]

        # 감성 점수의 차이가 최소인 순서로 정렬
        isbn_with_emotion_diff_sorted = sorted(isbn_with_emotion_diff, key=lambda x: x[1])

        # 차이가 가장 적은 상위 3권의 isbn 반환
        return [isbn for isbn, diff in isbn_with_emotion_diff_sorted[:3]]

    book_list_over_five=recommend_books_over_five_reviews(sentence, user_name, user_read, user_prefer_isbn, emotion)
    print(book_list_over_five)
    
    # 일단 사용자가 5권 이하를 읽었다고 했을 때 북 추천
    return emotion_result, book_list_under_five
    
