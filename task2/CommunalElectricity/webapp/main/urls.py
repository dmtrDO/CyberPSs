
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registration', views.registration, name='registration'),
    path('login', views.login, name='login'),
    path('home', views.home, name='home'),
    path('logout', views.logout, name='logout'),
    path('home/adding', views.add, name='add'),
    path('home/sending', views.send, name='send'),
    path('home/history', views.history, name='history')
]


