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
        return self.locality + ',' + self.city + ',' + self.state

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