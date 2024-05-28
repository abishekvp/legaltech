from django.urls import path
from . import views
from app import views as app_views

urlpatterns = [
    path('signout',app_views.signout,name="signout"),
    path('',views.index,name="master_admin"),
    path('happenings',app_views.happenings,name="happenings"),
]
