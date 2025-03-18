from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('our_doctors/', views.our_docts, name='our_docts'),
    path('doctor_page/', views.doctor_ui, name='doctor_ui'),
    path('update_address/', views.update_address, name='update_address'),
]