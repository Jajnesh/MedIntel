from django.shortcuts import render

# Create your views here.

# Home view
def home(request):
    return render(request,'homepage/index.html')

# Our Doctors View
def our_docts(request):
    return render(request,'homepage/our_doctors.html')

# Doctor UI
def doctor_ui(request):
    return render(request, 'doctor/index.html')