from django.contrib import admin
from django.utils.html import format_html
from .models import Doctor, Document, Patient, Appointment, Visit
from django_summernote.admin import SummernoteModelAdminMixin

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



class PatientAdmin(admin.ModelAdmin):
    model = Patient
    raw_id_fields = ('patient',)
    list_display = ('patient', 'full_name', 'email', 'date_of_birth', 'mobile_no', 'gender')
    search_fields = ('patient__username', 'patient__first_name', 'mobile_no')


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user','mobile','date','note','status')
    search_fields = ('user',)
    list_filter = ('status','date')
    list_editable = ('status',)
    ordering=('-date',)
    list_per_page = 25

class VisitInline(SummernoteModelAdminMixin, admin.StackedInline):
    model = Visit
    extra = 1
    summernote_fields = ('diagnosis',)
    fields = ('patient', 'doctor', 'diagnosis', 'created_at')
    readonly_fields = ('created_at',)

admin.site.register(Patient,PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Appointment,AppointmentAdmin)
