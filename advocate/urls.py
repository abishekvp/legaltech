from django.urls import path
from . import views
from app import views as app_views

urlpatterns = [
    path('signout',app_views.signout,name="signout"),
    path('',views.index,name="advocate-dashboard"),
    path('advocates',views.advocates,name="advocate-advocates"),
    path('profile',views.profile,name="advocate-profile"),
    path('advocate-contact',views.contact,name="advocate-contact"),
    path('advocate/<str:s>/',views.advocate_profile,name="profile"),
    path('happenings',views.happenings,name="happenings"),
    path('my-case',views.my_case,name="my-case"),
    path('advocate-messages',views.advocate_messages,name="advocate-messages"),
    path('chat-bot',app_views.chat_bot,name="chat-bot"),
    path('create-case',views.create_case,name="create-case"),
    path('advocate-case',views.advocate_case,name="advocate-case"),
    path('advocate-faq',views.faq,name="advocate-faq"),
]
