from django.urls import path
from . import views

urlpatterns = [
    path('recommendation/', views.recommendation),
    path('recommendation/result/', views.rec_result),
    path('recommendation/select/', views.rec_select),
]