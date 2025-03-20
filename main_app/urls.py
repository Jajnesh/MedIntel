from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('our_doctors/', views.our_docts, name='our_docts'),
    path('doctor_page/', views.doctor_ui, name='doctor_ui'),
    path('update_address/', views.update_address, name='update_address'),
    path('patient_page/', views.patient_ui, name='patient_ui'),
    path('delete_appointment/<int:aid>',views.delete_appointment,name="delete_appointment"),
    path('update_appointment/<int:aid>',views.update_appointment,name="update_appointment"),
    path('email_update/', views.email_update, name='email_update'),
    path('password_update/', views.password_update, name='password_update'),
]