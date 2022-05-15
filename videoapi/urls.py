from django.urls import path
from videoapi import views


urlpatterns = (
    path('', views.VideoList.as_view(), name='video-list'),
)