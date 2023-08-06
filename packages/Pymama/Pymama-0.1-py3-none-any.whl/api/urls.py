
from django.urls import path

from api import views






urlpatterns = [

    path('post/', views.snippet_list),
    path('post/<int:pk>/', views.snippet_detail),

]
