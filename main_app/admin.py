from django.contrib import admin
from .models import Doctor

# Register your models here.

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile_no', 'gender', 'medical_license_no', 'status', 'specialization', 'year_of_registration')
    list_filter = ('status', 'gender', 'specialization')
    search_fields = ('user__first_name', 'user__last_name', 'mobile_no', 'medical_license_no')
    ordering = ('user__first_name',)
    
    fieldsets = (
        (None, {
            'fields': ('user', 'mobile_no', 'gender', 'medical_license_no', 'registration_no', 'year_of_registration', 'qualification', 'specialization', 'state_medical_council', 'aadhar_no', 'status')
        }),
        ('Documents', {
            'fields': ('qualification_doc', 'aadhar_doc')
        }),
        ('Address', {
            'fields': ('prac_address',)
        }),
    )

admin.site.register(Doctor, DoctorAdmin)
