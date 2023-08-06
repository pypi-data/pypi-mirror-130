from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from tkm import views
from django.contrib.auth import views as auth_views
from tkm.forms import * 

from django.conf.urls import url

urlpatterns = [

path('',views.index,name="index"),
path('profile',views.profile,name="profile"),
path('login/', auth_views.LoginView.as_view(template_name='login.html',authentication_form=LoginForm),name='login'),
path('registration/', views.customerregistration, name='customerregistration'),
path('logout/',auth_views.LogoutView.as_view(next_page='login'),name="logout"),

path('dashboard',views.dashboard,name='dashboard'),

path('home', views.post_list, name='post_list'),

path('post/<int:pk>', views.post_detail, name='post_detail'),
path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    url(r'^post/new/$', views.post_new, name='post_new'),

]  
