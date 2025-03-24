from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('logout/', views.log_out, name='logout'),
    path('signup_doctor/', views.signup_doctor, name='signup_doctor'),
    path('signin_doctor/', views.signin_doctor, name='signin_doctor'),
    path('signup_patient/', views.signup_patient, name='signup_patient'),
    path('signin_patient/', views.signin_patient, name='signin_patient'),
    # Password reset views
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
