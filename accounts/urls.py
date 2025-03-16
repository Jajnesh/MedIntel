from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.log_out, name='logout'),
    path('signup_doctor', views.signup_doctor, name='signup_doctor'),
]
