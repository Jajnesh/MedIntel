from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.db import models
from main_app.models import Doctor, Address, Patient

# Create your views here.

# Home view
def home(request):
    return render(request,'homepage/index.html')

# Our Doctors View
def our_docts(request):
    # Get search queries from GET request
    doctor_name = request.GET.get('doctor-name', '').strip()
    specialization = request.GET.get('specialization', '').strip()
    locality = request.GET.get('locality', '').strip()
    
    doctors = Doctor.objects.filter(status='Approved')

    if doctor_name:
        doctors = doctors.filter(
            models.Q(user__first_name__icontains=doctor_name) | 
            models.Q(user__last_name__icontains=doctor_name)
        )

    if specialization:
        doctors = doctors.filter(specialization__icontains=specialization)

    if locality:
        doctors = doctors.filter(prac_address__locality__icontains=locality)

    doctors_found = doctors.exists()

    return render(request, 'homepage/our_doctors.html', {
        'doctors': doctors,
        'doctorname': doctor_name,
        'specialization': specialization,
        'locality': locality,
        'doctors_found': doctors_found,
    })

# Doctor UI
def doctor_ui(request):
    user_id = request.session.get('user_id', None)
    if user_id is None:
        messages.error(request, 'You are not logged in as a doctor.')
        return redirect('signin_doctor')

    user = User.objects.get(id=user_id)
    doctor = user.doctor

    return render(request, 'doctor/index.html', {'doctor': doctor})

# Patient UI
def patient_ui(request):
    user_id = request.session.get('user_id', None)
    if user_id is None:
        messages.error(request, 'You are not logged in as a patient.')
        return redirect('signin_patient')

    user = User.objects.get(id=user_id)
    patient = user.patient

    return render(request, 'patient/index.html', {'patient': patient})

# Update address
@login_required
def update_address(request):
    if request.method == 'POST':
        # Get the form data
        address_line_one = request.POST.get('address_line_one')
        locality = request.POST.get('locality')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')

        # Create or update the address
        address, created = Address.objects.update_or_create(
            address_line_one=address_line_one,
            locality=locality,
            city=city,
            state=state,
            country=country
        )

        # Update the doctor's practice address if it's the logged-in doctor
        doctor = Doctor.objects.get(user=request.user)
        doctor.prac_address = address
        doctor.save()

        return redirect('doctor_ui')

    messages.error(request, 'Invalid request.')
    return redirect('doctor_ui')
