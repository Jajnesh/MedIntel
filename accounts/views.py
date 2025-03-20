from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from main_app.models import Doctor, Document,Patient

# Create your views here.
def log_out(request):
    request.session.pop("user_id", None)
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
        qualification_doc = request.FILES.get('qualification_doc')
        state_medical_council = request.POST['state_medical_council']
        specialization = request.POST['specialization']
        other_specialization = request.POST.get('other_specialization', None)
        aadhar_no = request.POST['aadhar_no']
        aadhar_doc = request.FILES.get('aadhar_doc')

        if specialization == "other":
            specialization = other_specialization

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            print(f"Username '{username}' is already taken.")
            return redirect('signup_doctor')

        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken")
            print(f"Email '{email}' is already taken.")
            return redirect('signup_doctor')
        
        elif Doctor.objects.filter(aadhar_no=aadhar_no).exists():
            messages.error(request, "Aadhar no should be unique !!")
            print(f"Aadhar '{aadhar_no}' is already taken.")
            return redirect('signup_doctor')
        
        elif Doctor.objects.filter(medical_license_no=medical_license_no).exists():
            messages.error(request, "Already taken. Medical License no should be unique !!")
            print(f"License no'{medical_license_no}' is already taken.")
            return redirect('signup_doctor')
        
        elif Doctor.objects.filter(registration_no=registration_no, state_medical_council=state_medical_council).exists():
            messages.error(request, "Registration number should be unique within the same State Medical Council!")
            print(f"Registration no '{registration_no}' is already taken in '{state_medical_council}'.")
            return redirect('signup_doctor')


        else:
            user = User.objects.create_user(username=username, password=password, email=email, first_name=fname, last_name=lname)
            user.save()

            doc_description = f"Qualification Document for {fname} {lname}"
            qualification_document = Document(description=doc_description, document=qualification_doc)
            qualification_document.save()

            doc_description = f"Aadhar Document for {fname} {lname}"
            aadhar_document = Document(description=doc_description, document=aadhar_doc)
            aadhar_document.save()

            new_doctor = Doctor(
                user=user,
                gender=gender,
                mobile_no=mobile_no,
                medical_license_no=medical_license_no,
                registration_no=registration_no,
                year_of_registration=year_of_registration,
                qualification=qualification,
                qualification_doc = qualification_document,
                state_medical_council=state_medical_council,
                specialization=specialization,
                aadhar_no=aadhar_no,
                aadhar_doc=aadhar_document
            )
            new_doctor.save()

            messages.success(request, "Registration successful! Wait for admin approval.")
            return redirect('home')

@never_cache
def signin_doctor(request):
    if request.method == 'GET':
        return render(request, 'doctor/sign_in.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
               
        # Try to get the user object
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Invalid credentials')
            return redirect('signin_doctor')

        # If user exists, authenticate them
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if user is a doctor
            if hasattr(user, 'doctor'):
                if user.doctor.status == 'Approved':
                    login(request, user)
                    request.session['user_id'] = user.id
                    messages.success(request, 'Login Successfull')
                    return redirect('doctor_ui')
                elif user.doctor.status == 'Blocked':
                    messages.error(request, 'Sorry. Your account is blocked!. Kindly contact us for further enquiry.')
                    return redirect('signin_doctor')
                else:
                    messages.info(request, 'Please wait. Your approval is pending!')
                    return redirect('signin_doctor')
            else:
                messages.error(request, 'You are not a registered doctor.')
                return redirect('signin_doctor')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('signin_doctor')
        
# Patient authentication
def signup_patient(request):
    if request.method == "GET":
        return render(request, 'patient/sign_up.html')

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        date_of_birth = request.POST.get("dob")  # Get date of birth from form
        mobile_no = request.POST.get("mobile_no")
        gender = request.POST.get("gender")

        # Validation checks
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken!")
            return redirect('signup_patient')

        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email is already taken!")
            return redirect('signup_patient')
        elif Patient.objects.filter(mobile_no=mobile_no).exists():
            messages.error(request, "Mobile number is already registered!")
            return redirect('signup_patient')

        else:
            # Create User
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
            )
            user.save()

            # ✅ Create Patient Profile
            new_patient = Patient.objects.create(
                patient=user,
                date_of_birth=date_of_birth,
                mobile_no=mobile_no,
                gender=gender
            )
            new_patient.save()

            messages.success(request, "Registration successful! You can now log in.")
            return redirect('home')
        
@never_cache
def signin_patient(request):
    if request.method == "GET":
        return render(request, 'patient/sign_in.html')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Invalid credentials")
            return redirect('signin_patient')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if Patient.objects.filter(patient=user).exists():  # Check if Patient object exists
                login(request, user)
                request.session['user_id'] = user.id
                messages.success(request, 'Login Successfull')
                return redirect('home')  # Redirect patient to home or dashboard
            else:
                messages.error(request, "You are not registered as a patient.")
                return redirect('signin_patient')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('signin_patient')