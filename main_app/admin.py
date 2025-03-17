from django.contrib import admin
from django.utils.html import format_html
from .models import Doctor, Document

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile_no', 'gender', 'medical_license_no', 'status', 'specialization', 'year_of_registration', 'download_aadhar', 'download_qualification')
    list_filter = ('status', 'gender', 'specialization')
    search_fields = ('user__first_name', 'user__last_name', 'mobile_no', 'medical_license_no')
    ordering = ('user__first_name',)

    fieldsets = (
        (None, {
            'fields': ('user', 'mobile_no', 'gender', 'medical_license_no', 'year_of_registration', 'specialization', 'aadhar_no', 'status')
        }),
        ('Documents', {
            'fields': ('qualification_doc', 'aadhar_doc')
        }),
    )

    readonly_fields = [  # Make all fields read-only except 'status'
        'user', 'mobile_no', 'gender', 'medical_license_no', 'year_of_registration', 
        'specialization', 'aadhar_no', 'qualification_doc', 'aadhar_doc'
    ]

    def get_readonly_fields(self, request, obj=None):
        """Allows editing only the 'status' field."""
        if obj:  # If editing an existing record
            return self.readonly_fields  # Keep all fields read-only except 'status'
        return []  # Allow editing when creating a new record

    def download_aadhar(self, obj):
        """Creates a downloadable link for the Aadhar document."""
        if obj.aadhar_doc and obj.aadhar_doc.document:  # Corrected access to FileField
            return format_html('<a href="{}" target="_blank">View Aadhar Card</a>', obj.aadhar_doc.document.url)
        return "No document"
    download_aadhar.short_description = "Aadhar Card"

    def download_qualification(self, obj):
        """Creates a downloadable link for the Qualification document."""
        if obj.qualification_doc and obj.qualification_doc.document:  # Corrected access to FileField
            return format_html('<a href="{}" target="_blank">View Qualification</a>', obj.qualification_doc.document.url)
        return "No document"
    download_qualification.short_description = "Qualification Document"

admin.site.register(Doctor, DoctorAdmin)
