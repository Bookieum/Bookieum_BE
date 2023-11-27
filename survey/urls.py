from django.urls import path
from . import views


urlpatterns = [
    path('surveypage/', views.survey_page),
]
