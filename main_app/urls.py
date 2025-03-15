from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('our_doctors/', views.our_docts, name='our_docts'),
]