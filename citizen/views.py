from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.models import User, Group, Permission
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from app.views import db_user, meet_req, db_case
from django.contrib.auth.decorators import user_passes_test
import requests
from bs4 import BeautifulSoup
# Create your views here.
from app.views import db_chat

def is_citizen(user):
    return user.groups.filter(name='citizen').exists()    

def citizen_advocates(request):
    return render(request, 'citizen/advocates.html',{'advocates':User.objects.filter(groups__name__in=['advocate'])})

@user_passes_test(is_citizen)
def index(request):
    if request.user.is_authenticated:
        return render(request, 'citizen/dashboard.html')
    else:return redirect('signin')

def contact(request):
    return render(request, 'citizen/contact.html')

def chat_bot(request):
    import datetime
    if request.method=="POST":
        db_chat.insert_one({"user_message":request.POST.get("message"),"time_serires":datetime.datetime.now()})
        return "Reply Message"
    else:
        return render(request, 'citizen/chat-bot.html')

def message(request):
    return render(request, 'citizen/message.html')

def faq(request):
    return render(request, 'citizen/faq.html')

@user_passes_test(is_citizen)
def profile(request):
    return render(request, 'citizen/profile.html',{'profile':db_user.find_one({'username':request.user.username})})

def case(request):
    return render(request, 'citizen/case.html',{"cases":db_case.find()})

def view_advocate(request,name):
    return render(request, 'citizen/advocate-profile.html',{'profile':db_user.find_one({'username':name})})

def advocates(request):
    return render(request, 'citizen/advocates.html',{'advocates':db_user.find({'role':'advocate'})})

def request_meet(request, name):
    
    meet_req.insert_one({
        'advocate_name':name,
        'user_name':request.user.username
    })
    return redirect('citizen-advocates')

@user_passes_test(is_citizen)
def happenings(request):
    url = 'https://economictimes.indiatimes.com/topic/law-and-order'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        contents = soup.find_all('div',class_='contentD')
        image = soup.find_all('div',class_='imgD')
        data={}
        id=0
        for content,img in zip(contents,image):
            title = content.find('a')
            image = img.find('span')
            image = image.find('img')
            description = content.find('div',class_="wrapLines l3")
            data["content"+str(id)] = {
                "image":image.get("src"),
                "title":title.get("title"),
                "description":description.text
            }
            id+=1
        return render(request, 'citizen/happenings.html',{"data":data})
            
    else:
        messages.info(request, 'Error in fetching data from the website. Please try again later.')
    return render(request, 'citizen/happenings.html')
