from django.urls import path
from . import views

urlpatterns = [
    path('oauth/', views.google_login),
]
