from django.urls import path

from . import views

urlpatterns = [
    path('showVideo/',views.showVideo,name='showVideo'),
    path('stream',views.stream,name='video-feed'),
    path('deleteVideo/', views.delete, name='delete-video')

]