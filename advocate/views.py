from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User, Group, Permission
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from app.views import db_user, db_case, db_chat, happenings
from django.contrib.auth.decorators import user_passes_test
import requests
from bs4 import BeautifulSoup
# Create your views here.

def is_advocate(user):
    return user.groups.filter(name='advocate').exists()

def contact(request):
    return render(request, 'advocate/contact.html')

def chat_bot(request):
    import datetime
    if request.method=="POST":
        db_chat.insert_one({"user_message":request.POST.get("message"),"time_serires":datetime.datetime.now()})
        return "Reply Message"
    else:
        return render(request, 'advocate/chat-bot.html')

def advocate_messages(request):
    return render(request, 'advocate/message.html',{"messages":db_chat.find()})

def advocate_case(request):
    return render(request, 'advocate/case.html',{'cases':db_case.find()})

def message(request):
    return render(request, 'advocate/message.html')

def faq(request):
    return render(request, 'advocate/faq.html')

def get_data():
    url = 'https://economictimes.indiatimes.com/topic/law-and-order'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.find_all('div',class_='topicstry')
        data = []
        for i in divs:
            h2 = i.find('h2').text
            span = i.find('span')
            img = span.find('img')
            src = img.get('src')
            link = url+str(span.get('href'))
            data.append({
                "title":h2,
                "image":src,
                "url":link
            })
        return data
        # image = soup.find_all('div',class_='imgD')
        # print("images = ",image,"contents = ",contents)
        # data=[]
        # id=0
        # for content,img in zip(contents,image):
        #     title = content.find('a')
        #     print("title",title)
        #     image = img.find('span')
        #     image = image.find('img')
        #     description = content.find('div',class_="wrapLines l3")
        #     data.append({
        #         "image":image.get("src"),
        #         "title":title.get("title"),
        #         "description":description.text
        #     })
        #     id+=1
        # print(data)
        # return data
    else:
        return HttpResponse("Error in fetching data from the website. Please try again later.")
    


@user_passes_test(is_advocate)
def index(request):
    if request.user.is_authenticated:
        news = get_data()
        return render(request, 'advocate/dashboard.html',{"news_data":news,"advocates":db_user.find({"role":"advocate"})})
    else:return redirect('signin')

def advocate_profile(request):
    return render(request, 'advocate/profile.html')

@user_passes_test(is_advocate)
def profile(request):
    if request.method=="POST":
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        contact = request.POST['contact']
        dob = request.POST['dob']
        expertise = request.POST['expertise']
        success_count = request.POST['success_count']
        total_count = request.POST['total_count']
        experience_years = request.POST['experience_years']
        email = request.user.email
        db_user.update_one({"email":email},{
            "$set":{
                "firstname":f_name,
                "lastname":l_name,
                "contact":contact,
                "dob":dob,
                "expertise":expertise,
                "experience_years":int(experience_years),
                "success_count":int(success_count),
                "total_case":int(total_count)
            }
        })
        User.objects.filter(email=email).update(first_name=f_name,last_name=l_name)
        messages.info(request, 'Profile updated successfully.')
        
        return redirect('advocate-profile')
    
    return render(request, 'advocate/profile.html',{'profile':db_user.find_one({"email":request.user.email})})

def my_case(request):
    return render(request, 'advocate/my-case.html',{"cases":db_case.find({"advocate":request.user.username})})

def contact(request):
    return render(request, 'advocate/contact.html')

def create_case(request):
    import datetime
    if request.method=="POST":
        summary = request.POST['summary']
        label = request.POST['label']
        title = request.POST['title']
        case = {
            "summary":summary,
            "label":label,
            "title":title,
            "advocate":request.user.username,
            "email":request.user.email,
            "created_on":datetime.datetime.now()
        }
        db_case.insert_one(case)
        return redirect("advocate-case")
    else:
        return render(request, 'advocate/create-case.html' )

@user_passes_test(is_advocate)
def advocates(request):
    return render(request, 'advocate/advocates.html',{"advocates":db_user.find({"role":"advocate"})})

@user_passes_test(is_advocate)
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
        return render(request, 'advocate/happenings.html',{"data":data})
    else:
        messages.info(request, 'Error in fetching data from the website. Please try again later.')
    return render(request, 'advocate/happenings.html')
