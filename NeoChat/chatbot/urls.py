from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name ='chat'),
    path('send/', views.send_message, name='send_message')
]