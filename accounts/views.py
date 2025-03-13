from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache

from main_app.models import Doctor

# Create your views here.
def logout(request):
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
        name = request.POST['fname']
        gender = request.POST['gender']
        prac_address = request.POST['prac_address']
        mobile_no = request.POST['mobile']
        medical_license_no = request.POST['medical_license_no']
        qualification = request.POST['qualification']
        medical_uni = request.POST['medical_uni']
        specialization = request.POST['specialization']
        other_specialization = request.POST.get("other_specialization")

        if specialization == "other":
            specialization = other_specialization

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already taken")
            return redirect('signup_doctor')

        elif User.objects.filter(email=email).exists():
            messages.info(request, "Email already taken")
            return redirect('signup_doctor')

        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.status = 'Blocked'
            user.save()

            new_doctor = Doctor(
                user=user, name=name, gender=gender, prac_address=prac_address, 
                mobile_no=mobile_no, medical_license_no=medical_license_no, qualification=qualification,
                medical_uni=medical_uni, specialization=specialization
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