from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    name = models.CharField(max_length = 100)
    # prac_address = models.ForeignKey(Address, on_delete=models.SET_NULL)
    mobile_no = models.CharField(max_length = 20)
    gender = models.CharField(max_length = 10, choices=GENDER_CHOICES)
    medical_license_no = models.CharField(max_length = 20)
    qualification = models.CharField(max_length = 100)
    medical_uni = models.CharField(max_length = 100)
    specialization = models.CharField(max_length = 100)
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'