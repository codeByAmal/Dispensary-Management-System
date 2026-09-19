from django.db import models
import datetime

# Create your models here.
class Login(models.Model):
    login_id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=50)
    password=models.TextField(null=True)
    Usertype=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    class Meta:
        db_table='tbl_login'




class Complaint(models.Model):
    complaint_id=models.AutoField(primary_key=True)

    complaint=models.CharField(max_length=150)
    user_login_id=models.IntegerField()
    reply=models.CharField(max_length=50)
    class Meta:
        db_table='tbl_complaint'


class Lab(models.Model):
    lab_id=models.AutoField(primary_key=True)
    login_id=models.IntegerField()
    name=models.CharField(max_length=50)
    address=models.CharField(max_length=50, null=True)
    email=models.CharField(max_length=50)
    phone_number=models.BigIntegerField(null=True)
    place=models.CharField(max_length=50)

    class Meta:
        db_table='tbl_lab'
class Feedback(models.Model):
    feedback_id=models.AutoField(primary_key=True)
   
    feedback=models.CharField(max_length=150)
    user_login_id=models.IntegerField()
    reply=models.CharField(max_length=50)
    class Meta:
        db_table='tbl_feedback'

class Patients(models.Model):
    patient_id=models.AutoField(primary_key=True)
    login_id=models.IntegerField()
    patient_name=models.CharField(max_length=50, null=True)
    phone_number=models.BigIntegerField(null=True)
    Address=models.TextField()
    district_id=models.IntegerField()
    place=models.CharField(max_length=50, null=True)
    dob=models.DateField()
    entry_date=models.DateTimeField(default=datetime.datetime.now)
    class Meta:
        db_table='tbl_patient'

class Doctor(models.Model):
    doctor_id=models.AutoField(primary_key=True)
    login_id=models.IntegerField()
    doctor_first_name=models.CharField(max_length=50)
    doctor_last_name=models.CharField(max_length=50)
    address=models.CharField(max_length=50, null=True)
    email=models.CharField(max_length=50)
    phone_number=models.BigIntegerField(null=True)
    district_id=models.IntegerField()
    place=models.CharField(max_length=50)
    medical_speciality_id=models.IntegerField()
    qualification=models.CharField(max_length=50, null=True)
  
    photo=models.CharField(max_length=50)
    class Meta:
        db_table='tbl_doctor'
class MedicalSpeciality(models.Model):
    medical_speciality_id=models.AutoField(primary_key=True)
    speciality=models.CharField(max_length=50)
    class Meta:
        db_table='tbl_medical_speciality'

class Insurance(models.Model):
    insurance_id=models.AutoField(primary_key=True)
    insuarnce_company=models.CharField(max_length=50)
    description=models.CharField(max_length=500)
    class Meta:
        db_table='tbl_insurance'
class Appointment(models.Model):
    appointment_id=models.AutoField(primary_key=True)
    doctor_login_id=models.IntegerField()
    patient_login_id=models.IntegerField()
    appointment_date=models.DateField()
    entry_date=models.DateTimeField(default=datetime.datetime.now)
    status=models.CharField(max_length=50,default="Not Consulted")
    class Meta:
        db_table='tbl_appointment'

class prescription(models.Model):
    prescription_id=models.AutoField(primary_key=True)
    appointment_id=models.IntegerField()
    visiting_date=models.DateField()
    symptoms=models.TextField()
    medicine=models.TextField()
    uses=models.TextField()
    details=models.TextField()
    entry_date=models.DateTimeField(default=datetime.datetime.now)
    class Meta:
        db_table='tbl_prescription'
class lab_test_type(models.Model):
    lab_test_type_id=models.AutoField(primary_key=True)
    tests=models.CharField(max_length=50)
    lab_login_id=models.IntegerField()
    class Meta:
        db_table='tbl_lab_test_type'
class lab_test(models.Model):
    lab_test_id=models.AutoField(primary_key=True)
    appointment_id=models.IntegerField()
    test_id=models.IntegerField()
    status=models.CharField(max_length=50,default="Result is not Prepared")
    result=models.CharField(max_length=50,null=True)
    description=models.TextField(null=True)
    entry_date=models.DateTimeField(default=datetime.datetime.now)
    class Meta:
        db_table='tbl_lab_test'
class State(models.Model):
    state_id=models.AutoField(primary_key=True)
    country_id=models.IntegerField()
    state=models.CharField(max_length=50)
    class Meta:
        db_table='tbl_state'

class District(models.Model):
    district_id=models.AutoField(primary_key=True)
    state_id=models.IntegerField()
    district=models.CharField(max_length=50)
    class Meta:
        db_table='tbl_district'