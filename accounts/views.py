from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache

from main_app.models import Doctor

# Create your views here.
def log_out(request):
    request.session.pop("doctorusername", None)
    logout(request)
    return redirect('home')

# Doctor views
def signup_doctor(request):
    if request.method == 'GET':
        return render(request, 'doctor/sign_up.html')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        gender = request.POST['gender']
        mobile_no = request.POST['mobile']
        medical_license_no = request.POST['medical_license_no']
        registration_no = request.POST['registration_no']
        year_of_registration = request.POST['year_of_registration']
        qualification = request.POST['qualification']
        qualification_doc = request.POST['qualification_doc']
        state_medical_council = request.POST['state_medical_council']
        specialization = request.POST['specialization']
        other_specialization = request.POST['other_specialization']
        aadhar_no = request.POST['aadhar_no']
        aadhar_doc = request.POST['aadhar_doc']

        if specialization == "other":
            specialization = other_specialization

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already taken")
            return redirect('signup_doctor')

        elif User.objects.filter(email=email).exists():
            messages.info(request, "Email already taken")
            return redirect('signup_doctor')

        else:
            user = User.objects.create_user(username=username, password=password, email=email, first_name=fname, last_name=lname)
            user.save()

            new_doctor = Doctor(
                user=user,
                gender=gender,
                mobile_no=mobile_no,
                medical_license_no=medical_license_no,
                registration_no=registration_no,
                year_of_registration=year_of_registration,
                qualification=qualification,
                qualification_doc = qualification_doc,
                state_medical_council=state_medical_council,
                specialization=specialization,
                aadhar_no=aadhar_no,
                aadhar_doc=aadhar_doc
            )
            new_doctor.save()

            messages.info(request, "Registration successful! Wait for admin approval.")
            return redirect('home')

@never_cache
def signin_doctor(request):
    if request.method == 'GET':
       return render(request,'doctor/signin.html')

    if request.method == 'POST':
        username =  request.POST.get('username')
        password =  request.POST.get('password')
        user = authenticate(request, username=username,password=password)

        if user is not None :
            if ( user.doctor.status == 'Approved' ) :
                login(request,user)
                request.session['doctorusername'] = user.username
                return redirect('doctor_ui')
            else :
                messages.info(request,'Please wait. Your approval is pending!!')
                return redirect('signin_doctor')

        else :
            messages.info(request,'Invalid credentials')
            return redirect('signin_doctor')