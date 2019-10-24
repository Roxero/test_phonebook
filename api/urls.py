from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "api"

urlpatterns = [
    path('entries/', views.PersonList.as_view()),
    path('entries/<int:pk>/', views.PersonDetail.as_view()),
]
