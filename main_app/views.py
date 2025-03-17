from django.shortcuts import render

from django.db import models
from main_app.models import Doctor

# Create your views here.

# Home view
def home(request):
    return render(request,'homepage/index.html')

# Our Doctors View
def our_docts(request):
    search_query = request.GET.get('doctor-search', '')
    
    doctors = Doctor.objects.filter(status='Approved')

    if search_query:
        doctors = doctors.filter(
            models.Q(user__first_name__icontains=search_query) | 
            models.Q(user__last_name__icontains=search_query) | 
            models.Q(specialization__icontains=search_query)
        )

    doctors_found = doctors.exists()

    return render(request, 'homepage/our_doctors.html', {
        'doctors': doctors,
        'search_query': search_query,
        'doctors_found': doctors_found,
    })

# Doctor UI
def doctor_ui(request):
    return render(request, 'doctor/index.html')