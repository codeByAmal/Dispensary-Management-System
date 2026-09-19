from django.contrib import admin
from .models import (
    Login,
    Complaint,
    Lab,
    Feedback,
    Patients,
    Doctor,
    MedicalSpeciality,
    Insurance,
    Appointment,
    prescription,
    lab_test_type,
    lab_test,
    State,
    District,
)

admin.site.register(Login)
admin.site.register(Complaint)
admin.site.register(Lab)
admin.site.register(Feedback)
admin.site.register(Patients)
admin.site.register(Doctor)
admin.site.register(MedicalSpeciality)
admin.site.register(Insurance)
admin.site.register(Appointment)
admin.site.register(prescription)
admin.site.register(lab_test_type)
admin.site.register(lab_test)
admin.site.register(State)
admin.site.register(District)