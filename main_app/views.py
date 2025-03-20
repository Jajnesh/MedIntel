from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django import forms
from django.db import models, transaction
from main_app.models import Doctor, Address, Patient, Appointment, Visit
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

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
@login_required(login_url='accounts:signin_doctor')
def doctor_ui(request):
    if not hasattr(request.user, 'doctor'):  # Ensure the user is a doctor
        messages.error(request, 'You are not logged in as a doctor.')
        return redirect('signin_doctor')

    return render(request, 'doctor/index.html', {'doctor': request.user.doctor})

# Patient UI
def patient_ui(request):
    user_id = request.session.get('user_id', None)
    if user_id is None:
        messages.error(request, 'You are not logged in as a patient.')
        return redirect('signin_patient')

    user = User.objects.get(id=user_id)

    # ✅ Check if user has a related patient object
    patient = getattr(user, 'patient', None)  
    if patient is None:
        messages.error(request, 'You do not have a patient profile.')
        return redirect('home')  # Redirect to home or another appropriate page

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


@login_required(login_url='accounts:signin_patient')
def profile(request):
    patient = Patient.objects.filter(patient=request.user).first()  # Get patient safely

    visits = Visit.objects.filter(patient=patient) if patient else []  # Fetch visits if patient exists

    context = {
        'patient': patient,
        'visits': visits,
    }

    return render(request, 'patient/index.html', context)


@login_required(login_url='accounts:signin_patient')
def appointment(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        date = request.POST.get('date')
        note = request.POST.get('note')

        # Check if user already has an appointment for that date
        if Appointment.objects.filter(user=request.user, date=date).exists():
            messages.error(request, f"You already have an appointment on {date}.")
        # Limit slots to 20 per day
        elif Appointment.objects.filter(date=date).count() >= 20:
            messages.error(request, f"All slots for {date} are booked.")
        else:
            Appointment.objects.create(user=request.user, mobile=mobile, date=date, note=note)
            messages.success(request, "Appointment booked successfully!")

    # Get all appointments of logged-in user
    appointments = Appointment.objects.filter(user=request.user).order_by('-date')
    return render(request, 'patient/appointment.html', {'appointments': appointments})


@login_required(login_url='accounts:signin_patient')
def delete_appointment(request, aid):
    appointment = get_object_or_404(Appointment, id=aid, user=request.user)
    appointment.delete()
    messages.success(request, "Appointment deleted successfully.")
    return redirect('appointment')


@login_required(login_url='accounts:signin_patient')
def update_appointment(request, aid):
    appointment = get_object_or_404(Appointment, id=aid, user=request.user)

    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        date = request.POST.get('date')
        note = request.POST.get('note')

        # Check if the new date is already taken
        if Appointment.objects.filter(user=request.user, date=date).exclude(id=aid).exists():
            messages.error(request, f"You already have an appointment on {date}.")
        elif Appointment.objects.filter(date=date).count() >= 20:
            messages.error(request, f"All slots for {date} are booked.")
        else:
            with transaction.atomic():  # Ensures the update is done safely
                appointment.mobile = mobile
                appointment.date = date
                appointment.note = note
                appointment.save()
                messages.success(request, "Appointment updated successfully!")
                return redirect('appointment')

    return render(request, 'patient/appointment_update.html', {'appointment': appointment})

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

@login_required
def email_update(request):
    if request.method == "POST":
        email_form = EmailChangeForm(request.POST, instance=request.user)
        if email_form.is_valid():
            email_form.save()
            messages.success(request, "Email Updated Successfully")

            # Redirect based on user type
            if hasattr(request.user, 'patient'):  
                return redirect('patient_ui')
            elif hasattr(request.user, 'doctor'):
                return redirect('doctor_ui')
            else:
                return redirect('home')

    else:
        email_form = EmailChangeForm(instance=request.user)

    # Render the appropriate template based on user type
    if hasattr(request.user, 'doctor'):  
        return render(request, 'doctor/email_update.html', {'email_form': email_form})
    else:
        return render(request, 'patient/email_update.html', {'email_form': email_form})

# @login_required
# def password_update(request):
#     if request.method == "POST":
#         password_form = PasswordChangeForm(request.user, request.POST)
#         if password_form.is_valid():
#             password_form.save()
#             update_session_auth_hash(request, request.user)  # Keeps the user logged in after password change
#             messages.success(request, "Password Updated Successfully")

#             # Redirect based on user type
#             if hasattr(request.user, 'patient'):  
#                 return redirect('patient_ui')
#             elif hasattr(request.user, 'doctor'):
#                 return redirect('doctor_ui')
#             else:
#                 return redirect('home')
#     else:
#         password_form = PasswordChangeForm(request.user)

@login_required
def password_update(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")

        if not request.user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
        elif new_password1 != new_password2:
            messages.error(request, "New passwords do not match.")
        else:
            request.user.set_password(new_password1)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Password Updated Successfully")

            # Redirect based on user type
            return redirect("doctor_ui" if hasattr(request.user, "doctor") else "patient_ui")

    # Render the appropriate template
    template = "doctor/password_update.html" if hasattr(request.user, "doctor") else "patient/password_update.html"
    return render(request, template)


    # Render the appropriate template based on user type
    if hasattr(request.user, 'doctor'):  
        return render(request, 'doctor/password_update.html', {'password_form': password_form})
    else:
        return render(request, 'patient/password_update.html', {'password_form': password_form})
