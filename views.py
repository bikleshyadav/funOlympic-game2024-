from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from datetime import datetime
from .models import *
import random

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from .forms import CustomPasswordChangeForm


from django.contrib.auth.decorators import login_required

from .forms import User,ProfileForm,CreateUserForm
# Create your views here.
date=datetime.now().year

def home(request):
    v=Video.objects.all()
    current_date=datetime.now()

    context={
        'current_date':current_date,
        'date':date,
        'v':v
    }
    return render(request,'myApp/home.html',context)

def register(request):
    form=CreateUserForm()

    if request.method == 'POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request,"Account is created")
            return redirect('log_in')
        else:
            context={'form':form}
            messages.info(request,form.errors)
            return render(request,'auth/register.html',context)
        # username=request.POST['name']
        # email = request.POST['email']
        # password = request.POST['password']
        # password1 = request.POST['password1']
        # if password == password1:
            
        #     if User.objects.filter(email=email).exists():
        #         messages.success(request, f'{email} Is Already Exist')
        #         return redirect('register')
        #     elif User.objects.filter(username=username).exists():
        #         messages.success(request, f'{username} Is Already Exist')
        #         return redirect('register')
        #     else:
        #         user = User.objects.create_user(username=username, email=email, password=password)
        #         # user.set_password(password)
        #         user.save()
        #     return redirect('log_in')
        # else:
        #     messages.info(request, f'{username} your password not match!!!')
        #     return redirect('register')
    context={
        'form':form
    }
    
    return render(request, 'auth/register.html',context)

        
def log_in(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"password is invalid")
            return redirect('log_in')

    return render(request,'auth/login.html')


def log_out(request):
    logout(request)
    return redirect('log_in')


def news(request):
    popular=Post.objects.filter(section='Popular').order_by('-id')[0:4]
    recent=Post.objects.filter(section='Recent').order_by('-id')[0:4]
    trending=Post.objects.filter(section='Trending').order_by('-id')[0:3]
    latest=Post.objects.filter(section='Latest Post').order_by('-id')[0:3]
    main=Post.objects.filter(main_post=True)[0:1]
    

    context={
        'popular':popular,
        'recent':recent,
        'main':main,
        'trending':trending,
        'latest':latest
    }

    return render(request,'myApp/news.html',context)

@login_required(login_url='log_in')
def live(request):
    data = get_object_or_404(Profile, user=request.user)
    context = {
        'username': request.user.username,
        'profile': data,
    }
    return render(request, "MyApp/stream.html",context)




def single(request,id):
    post = get_object_or_404(Post, id=id)
    popular=Post.objects.filter(section='Popular').order_by('-id')[0:4]
    data=Post.objects.all()
    msg=Comment.objects.all().order_by('-id')[:3]
    context={
        'post':post,
        'popular':popular,
        'data':data,
        'msg':msg
    }
    if request.method=='POST':
        name=request.POST['name']
        comment=request.POST['comment']

        msg=Comment(name=name,comment=comment)
        msg.save()
        messages.success(request,"successfully comment!!!")
        return redirect('single',id=id)
    


    return render(request,'myApp/single.html',context)

def contact(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        phone=request.POST['phone']
        message=request.POST['message']

        form=Contact_form(fname=fname,lname=lname,email=email,phone=phone,message=message)
        form.save()
        messages.success(request,"Successfully send!!!!")
        return redirect('contact')
    return render(request,'myApp/contact.html')
def event(request):
    return render(request,'myApp/event.html')

# @login_required(login_url='log_in')
def profileupdate(request):
    profile = request.user.profile  # Assuming user is authenticated
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile view page
    else:
        form = ProfileForm(instance=profile)
    context={'form':form}
    return render(request,'myApp/profileupdate.html',context)
def profile(request):
    return render(request,'myApp/profile.html')


def event(request):
    event = Events.objects.all()
    return render(request, "myApp/event.html", {'username': request.user.username, "event" : event})


def player(request,title):
    data = get_object_or_404(Video, title=title)
    data.views += 1
    data.save()
    comments = Comment.objects.filter(video=data.id)
    total_comments = comments.count()
    all_videos = Video.objects.exclude(title=title)
    random_videos = random.sample(list(all_videos), min(3, len(all_videos)))
    if request.method == 'POST':
        video = data
        user = request.user
        text = request.POST['text']
        comment = Comment.objects.create(video=video, user=user, text=text)
        comment.save()

    return render(request, "myApp/player.html",{'data': data,"video": random_videos, 'comments': comments, 'total_comments': total_comments })


def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to maintain session
            return redirect('log_in')  # Redirect to a success page
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'auth/change_password.html', {'form': form})

