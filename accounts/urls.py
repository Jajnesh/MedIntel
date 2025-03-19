from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.log_out, name='logout'),
    path('signup_doctor/', views.signup_doctor, name='signup_doctor'),
    path('signin_doctor/', views.signin_doctor, name='signin_doctor'),
    path('signup_patient/', views.signup_patient, name='signup_patient'),
    path('signin_patient/', views.signin_patient, name='signin_patient'),
]
