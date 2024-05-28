from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User, Group, Permission
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import datetime
import requests
from bs4 import BeautifulSoup

url = "mongodb://localhost:27017"
# url = "mongodb+srv://pro_user:rkwyrUiPnjjBsssg@cluster0.edxis.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(url, server_api=ServerApi('1'))

# admin abishek 123

db = client.legaltech
db_user = db.users
db_chat = db.user_chat
db_case = db.case
meet_req = db.meet_req 

def advocate_profile(request, username):
    advocate = db_user.find_one({"username":username})
    return render(request, 'advocate-profile.html', {"advocate":advocate})


def message_proccess(input):
    input=str(input).lower()

    def proccess(input):
        if input=="hi" or input=="hello":
            return "Hello! How can I help you?"
        elif input=="how are you?":
            return "I am a bot. I am always fine."
        else:
            return "I am sorry, I don't understand."
        
    proccessed_message = proccess(input)
    
    return proccessed_message

def chat_message(request):
    user_message = request.POST.get("message")
    bot_message = message_proccess(user_message)
    db_chat.insert_one({"user_message":user_message,"time_serires":datetime.datetime.now()})
    db_chat.insert_one({"bot_message":bot_message,"time_serires":datetime.datetime.now()})
    print(bot_message)
    return HttpResponse(bot_message)

def chat_bot(request):
    if request.method=="POST":
        db_chat.insert_one({"user_message":request.POST.get("message"),"time_serires":datetime.datetime.now()})
        return "Reply Message"
    else:
        return render(request, 'citizen/chat-bot.html')

def index(request):
    return redirect('signup')

def auth_route(request):
    role=request.user.groups.all().first().name
    if role == "admin":return redirect("master_admin")
    elif role == "citizen":return redirect("citizen-dashboard")
    elif role == "advocate":return redirect("advocate-dashboard")
    else:return redirect("signin")

def signup(request):
    if request.user.is_authenticated:return redirect('auth_route')
    elif request.method=="POST":
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        if User.objects.filter(username=username).exists():messages.info(request, 'Username already exists')
        elif User.objects.filter(email=email).exists():messages.info(request, 'Email already exists')
        else:
            user = User.objects.create_user(first_name=name, username=username, email=email, password=password)
            user = db_user.insert_one({
                "name":name,
                "username":username,
                "email":email,
                "role":role,
                "password":password,
                "bar_code":0,
                "experiance":0,
                "contact":0,
                "country":"",
                "state":"",
                "city":"",
                "total_case":0,
                "success":0,
                "speacilized":"crime",
                "description":""
            })
            user = authenticate(request, username=username, password=password)
            group = Group.objects.all().filter(name=role).first()
            user = User.objects.get(username=username)
            user.groups.add(group)
            login(request, user)
            return redirect('auth_route')
        return redirect("signup")
    else:return render(request,'./sign/signup.html')

def signin(request):
    if request.user.is_authenticated:return redirect('auth_route')
    elif request.method == 'POST':    
        username = request.POST["email"]
        password = request.POST["password"]
        if '@' in username:username = User.objects.get(email=username.lower()).username
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            role=User.objects.get(username=username).groups.all().first().name
            return redirect('auth_route')
            
        else:messages.info(request, 'User not found')
        return redirect("signin")
    else:return render(request,'./sign/signin.html')

def signout(request):
    if request.user.is_authenticated:logout(request)
    return redirect('signin')

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
        print(data)
        return data
    else:
        return HttpResponse("Error in fetching data from the website. Please try again later.")
    