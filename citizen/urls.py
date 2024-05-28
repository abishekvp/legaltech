from django.urls import path
from . import views
from app import views as app_views

urlpatterns = [
    path('signout',app_views.signout,name="signout"),
    path('',views.index,name="citizen-dashboard"),
    path('citizen-profile',views.profile,name="citizen-profile"),
    path('advocates',views.advocates,name="citizen-advocates"),
    path('happenings',views.happenings,name="happenings"),
    path('contact',views.contact,name="citizen-contact"),
    path('message',views.message,name="citizen-message"),
    path('faq',views.faq,name="citizen-faq"),
    path('citizen-chat-bot',views.chat_bot,name="citizen-chat-bot"),
    path('view-advocate/<str:name>/',views.view_advocate,name="view-advocate"),
    path('request-meet/<str:name>/',views.request_meet,name="request-meet"),
    path('case',views.case,name="case"),
]

