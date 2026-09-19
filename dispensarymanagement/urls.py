"""
URL configuration for hospitalmanagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dispensaryapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.index),
    path('index/',views.index),
    path('login_action/', views.sign_in_process),
    path('hospital_registration/', views.hospital_registration),
    path('patient_registration/', views.patient_registration),
    path('admin_home/', views.admin_home),
    path('lab_home/', views.lab_home),
    path('doctor_home/', views.doctor_home),
    path('patient_home/', views.patient_home),
 
     

    
    path('admin_logout/', views.admin_logout),
    path('user_logout/',views.user_logout),
    path('sign_in/',views.sign_in),
    path('display_district/', views.display_district, name='display_district'),
    path('save_hospital/', views.hospital_action),
    path('save_patient/', views.patient_action),
    path('login/',views.sign_in),

    # Approval - hospital

    path('approve_hospital/', views.approve_hospital),
    path('approve/<int:id>', views.approve),
    path('reject/<int:id>', views.reject),
    path('hospital_list/', views.hospital_list),
 
    #Complaints
    path('view_complaints/', views.view_complaints),
    path('replied_list/', views.replied_list),
    path('adm_reply_complaint/<int:id>', views.adm_reply_complaint),
    path('add_reply/<int:id>', views.add_reply),


   #feedback
    path('view_feedback/', views.view_feedback),
    path('feedback_replied_list/', views.feedback_replied_list),
    path('adm_reply_feedback/<int:id>', views.adm_reply_feedback),
    path('add_reply_feedback/<int:id>', views.add_reply_feedback),
    

    #  Customer
    path('add_complaint/', views.Complaint_frm),
    path('save_complaint/', views.save_complaint),
    path('delete_complaint/<int:id>', views.delete_complaint),

    path('feedback/', views.feedback_frm),
    path('save_feedback/', views.save_feedback),
    path('delete_feedback/<int:id>', views.delete_feedback),
    #Doctor
    path('add_doctor/', views.add_doctor),
    path('save_Doctor/', views.save_doctor),
    path('doctor_list/', views.doctor_list),
    path('edit_doctor/<int:id>', views.edit_doctor),
    path('update_doctor/<int:id>', views.update_doctor),
    path('delete_doctor/<int:id>', views.delete_doctor),


    path('add_insurance/', views.add_insurance),
    path('save_insurance/', views.save_insurance),
    path('edit_insurance/<int:id>', views.edit_insurance),
    path('update_insurance/<int:id>', views.update_insurance),
    path('delete_insurance/<int:id>', views.delete_insurance),
      
    #pATIENT


    path('appointment/', views.appointment),
    path('display_doctor/', views.display_doctor, name='display_doctor'),
    path('display_speciality/', views.display_speciality, name='display_speciality'),
    path('save_appointment/', views.save_appointment),
    path('history/', views.history),
    path('display_hospital_list/', views.display_hospital_list, name='display_hospital_list'),
    path('doctors/<int:id>', views.doctors),
    path('insurance/<int:id>', views.insurance),
    path('patient_profile/', views.patient_profile),
    path('update_profile/<int:id>', views.update_profile),
    path('patient_change_password/', views.patient_change_password),
    path('update_password/', views.update_password),
    path('patient_list/', views.patient_list),
    path('appointment_list/', views.appointment_list),

    # Doctor

    path('appointment_approval/', views.appointment_approval),
    path('new_appointment/', views.new_appointment),
    path('add_prescription/<int:id>', views.add_prescription),
    path('save_prescription/<int:id>', views.save_prescription),
    path('all_appointment_list/', views.all_appointment_list),
    path('view_prescription/<int:id>', views.view_prescription),
    path('new_appointment/', views.new_appointment),
    path('dr_view_patient/', views.dr_view_patient),
    path('dr_view_patient_records/<int:id>', views.dr_view_patient_records),
    

    path('appointment_status/', views.appointment_status),

    path('approve_appointment/<int:id>', views.approve_appointment),
     path('reject_appointment/<int:id>', views.reject_appointment),
    
    path('doctor_profile/', views.doctor_profile),
    path('update_dr_profile/<int:id>', views.update_dr_profile),
    path('change_password_doctor/', views.change_password_doctor),
    path('update_dr_password/', views.update_dr_password),
    
    path('add_speciality/', views.add_speciality),
    path('save_speciality/', views.save_speciality),
    path('edit_speciality/<int:id>', views.edit_speciality),
    path('update_speciality/<int:id>', views.update_speciality),
    path('delete_speciality/<int:id>', views.delete_speciality),

    

     path('view_prescription_patient/<int:id>', views.view_prescription_patient),

     #Lab
    path('add_lab/', views.add_lab),
    path('save_lab/', views.save_lab),
    path('lab_details/', views.lab_details),
    path('edit_lab/<int:id>', views.edit_lab),
    path('update_lab/<int:id>', views.update_lab),
    path('delete_lab/<int:id>', views.delete_lab),

    path('add_test_type/', views.add_test_type),
    path('save_test_type/', views.save_test_type),
    path('edit_test_type/<int:id>', views.edit_test_type),
    path('update_test_type/<int:id>', views.update_test_type),
    path('delete_test_type/<int:id>', views.delete_test_type),
    path('display_lab_type/', views.display_lab_type, name='display_lab_type'),

    path('view_test_list/', views.view_test_list),
    path('add_test_result/<int:id>', views.add_test_result),
    path('save_test_result/<int:id>', views.save_test_result),
    path('view_test_result/', views.view_test_result),
    

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
