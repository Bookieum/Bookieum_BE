from django.urls import path
from . import views


urlpatterns = [
    path('information/', views.user_information),
    path('detail/',views.book_detail),
    path('book/progress/',views.book_progress),
]

