from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name="signup"),
    path('auth_route',views.auth_route,name="auth_route"),
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('signout',views.signout,name="signout"),
    path('chat_message',views.chat_message,name="chat_message"),
    path('chat-bot',views.chat_bot,name="chat-bot"),
]
