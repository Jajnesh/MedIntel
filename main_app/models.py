from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.description
    
    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'


class Address(models.Model):
    address_line_one = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.address_line_one + ', ' + self.locality + ', ' + self.city + ', ' + self.state

class Doctor(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Blocked', 'Blocked')
    ]
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor')
    prac_address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, null=True, blank=True)
    mobile_no = models.CharField(max_length = 20)
    gender = models.CharField(max_length = 10, choices=GENDER_CHOICES)
    medical_license_no = models.CharField(max_length = 20, unique=True)
    registration_no = models.CharField(max_length = 20, default='000000', unique=True)
    year_of_registration = models.IntegerField(default=2025)
    qualification = models.CharField(max_length = 100)
    qualification_doc = models.ForeignKey(Document, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='qualification_docs')
    state_medical_council = models.CharField(max_length = 100)
    specialization = models.CharField(max_length = 100)
    aadhar_no = models.CharField(max_length=30, default='000000', unique=True)
    aadhar_doc = models.ForeignKey(Document, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='aadhar_doc')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.user.first_name
    
    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

class Patient(models.Model):
    patient = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    date_of_birth = models.DateField()
    background_history = models.TextField(default="", blank=True)
    mobile_no = models.CharField(max_length=10, unique=True, null=True, blank=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.patient.username
    def full_name(self):
        return f"{self.patient.first_name} {self.patient.last_name}"
    def email(self):
        return f"{self.patient.email}"
    
APPOINTMENT_STATUS_OPTIONS = {
    'Booked':'Booked',
    'Visited':'Visited',
    'Canceled':'Canceled'
}

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)  # Patient
    # doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20)
    date = models.DateField()
    note = models.TextField()
    status = models.CharField(max_length=255, choices=APPOINTMENT_STATUS_OPTIONS, default="Booked")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
class Visit(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    diagnosis = models.TextField()

    def __str__(self):
        return f"{self.created_at}"