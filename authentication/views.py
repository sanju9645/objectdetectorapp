
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def home(request):
    return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        full_name=request.POST['fname']
        user_name=request.POST['userName']
        password1=request.POST['password1']
        email=request.POST['email']
                
        if User.objects.filter(username=user_name).exists():
            return redirect("/?message=User exists")

        user = User.objects.create_user(user_name,email,password1)
        if not user:
            return redirect("/?message=Something went wrong")
        
        user.first_name=full_name
        user.save()
        return redirect('/?message=Succesfully Registered,Please signin to continue')
        
    else:
        return HttpResponse('404 - Not Found')
    
@csrf_exempt
def signin(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('showVideo')
        else:
            
            return redirect('/?message=Invalid Credentials ! ! !')
    return HttpResponse('login/')

def signout(request):
    logout(request)

    return redirect('/?message=Succesfully Logged Out')

    return HttpResponse('signout')