from django.shortcuts import render,redirect,HttpResponse
from django.http.response import StreamingHttpResponse
from .models import Video
from .forms import VideoForm

import numpy as np
import numpy.core.multiarray
import cv2, random

from YoloDetector import YoloDetector
# Create your views here.

def showVideo(request):
    if request.user.is_authenticated:
        
        form= VideoForm(request.POST or None, request.FILES or None)
        #form= VideoForm(request.FILES or None)
        
        if request.method=='POST':
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user=request.user
                obj.save()

        lastvideo= Video.objects.filter(user=request.user)

        if lastvideo.exists():
            lastvideo=lastvideo.last()
            videofile=lastvideo.videofile
            lastvideo_id = lastvideo.id
    
        else:
            videofile="/media/videos/input_video.mp4"
            lastvideo_id = -1
            
        #videofile= lastvideo.videofile
        with open("./coco.names", 'r') as f:
            classes = [w.strip() for w in f.readlines()]
        
        context= {'videofile': videofile,'form': form,'video_id':lastvideo_id, 'classes':classes}
        
        return render(request, 'videoUpload.html', context)
    else:
        return redirect('/?404 - Not Found ! ! !')
        return HttpResponse('404 - Not Found')

def videoFeed(source,selected_classes):
    with open("./coco.names", 'r') as f:
        classes = [w.strip() for w in f.readlines()]
    
    detector = YoloDetector("./yolov3-tiny.cfg", "./yolov3-tiny.weights", classes)
    
    vid=cv2.VideoCapture(source)
    
    selected={}
    
    for cls in selected_classes:
        selected[cls]=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    
    # selected = {"person": (0, 255, 255),
    #             "laptop": (0, 0, 0),
    #             "apple": (0, 255, 255)}
    
    
    while vid.isOpened():
        ret,frame=vid.read()
        
        detections = detector.detect(frame)
        
        for cls, color in selected.items():
            if cls in detections:
                for box in detections[cls]:
                    x1, y1, x2, y2 = box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness=1)
                    cv2.putText(frame, cls, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color)
            
        cv2.imwrite('demo.jpg', frame)
        yield (b'--frame\r\n'+b'Content-Type: image/jpeg\r\n\r\n' + open('demo.jpg', 'rb').read() + b'\r\n')

def stream(request):
    id=request.GET.get('id')
    classes=request.GET.get('classes')
    if not classes:
        classes=[]
    else:
        classes=classes.split(',')


    if not Video.objects.filter(id=id).exists():
        source = "media/videos/input_video.mp4"
    else:
        source = Video.objects.get(id=id).videofile.path
    return StreamingHttpResponse(videoFeed(source,classes), content_type='multipart/x-mixed-replace; boundary=frame')

def clearVideos(user):
    user_uploaded_videos=Video.objects.filter(user=user)
    user_uploaded_videos._raw_delete(user_uploaded_videos.db)

def delete(request):
    if request.user.is_authenticated:
        clearVideos(request.user)
        return redirect('showVideo')
        
    else:
        return redirect('/?404 - Not Found ! ! !')
        return HttpResponse('404 - Not Found')