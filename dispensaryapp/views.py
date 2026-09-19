import os
from datetime import date, datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.core.files.storage import FileSystemStorage
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from dispensaryapp.models import *


# Create your views here.
def index(request):
    return render(request,'index.html')

def hospital_registration(request):
    data = State.objects.all()
    return render(request,'hospital_registration.html',{'data':data})

def patient_registration(request):
    today1 = date.today()
    data = State.objects.all()
    return render(request,'patient_registration.html',{'data':data,'today':today1})

def sign_in(request):
    return render(request,'signin.html')

def sign_in_process(request):
    u=request.POST.get("username")
    p=request.POST.get("password")
    obj=authenticate(username=u,password=p)
    if obj is not None:
        if obj.is_superuser == 1:
            request.session['aname'] = u
            request.session['slogid'] = obj.id
            return redirect('/admin_home/')
        else:
          messages.add_message(request, messages.INFO, 'Invalid User.')
          return redirect('/index/')
    else:
        newp=p
        try:
            obj1=Login.objects.get(username=u,password=newp)

            if obj1.Usertype=="Lab":
                if(obj1.status=="Approved"):
                    request.session['lname'] = u
                    request.session['slogid'] = obj1.login_id
                    return redirect('/lab_home/')
                elif(obj1.status=="Not Approved"):
                  messages.add_message(request, messages.INFO, 'Waiting For Approval.')
                  return redirect('/login/')
                else:
                  messages.add_message(request, messages.INFO, 'Invalid User.')
                  return redirect('/login/')
            elif obj1.Usertype=="Doctor":
                if(obj1.status=="Approved"):
                    request.session['dname'] = u
                    request.session['slogid'] = obj1.login_id
                    return redirect('/doctor_home/')
                elif(obj1.status=="Not Approved"):
                  messages.add_message(request, messages.INFO, 'Waiting For Approval.')
                  return redirect('/login/')
                else:
                  messages.add_message(request, messages.INFO, 'Invalid User.')
                  return redirect('/login/')
            elif obj1.Usertype=="Patient":
                if(obj1.status=="Approved"):
                    request.session['pname'] = u
                    request.session['slogid'] = obj1.login_id
                    return redirect('/patient_home/')
                elif(obj1.status=="Not Approved"):
                  messages.add_message(request, messages.INFO, 'Waiting For Approval.')
                  return redirect('/login/')
                else:
                  messages.add_message(request, messages.INFO, 'Invalid User.')
                  return redirect('/login/')
            elif obj1.Usertype=="Receptionist":
                if(obj1.status=="Approved"):
                    request.session['cname'] = u
                    request.session['slogid'] = obj1.login_id
                    return redirect('/receptionist_home/')
                elif(obj1.status=="Not Approved"):
                  messages.add_message(request, messages.INFO, 'Waiting For Approval.')
                  return redirect('/login/')
                else:
                  messages.add_message(request, messages.INFO, 'Invalid User.')
                  return redirect('/login/')

            else:
                 messages.add_message(request, messages.INFO, 'Invalid User.')
                 return redirect('/login/')
        except Login.DoesNotExist:
         messages.add_message(request, messages.INFO, 'Invalid User.')
         return redirect('/login/')

def admin_home(request):
    if 'aname' in request.session:
     return render(request,'Master/index.html')
    else:
      return redirect('/index/')

def lab_home(request):
    if 'lname' in request.session:
     return render(request,'Lab/index.html')
    else:
      return redirect('/index/')

def doctor_home(request):
    if 'dname' in request.session:
     return render(request,'Doctor/index.html')
    else:
      return redirect('/index/')

def patient_home(request):
    if 'pname' in request.session:
        cursor=connection.cursor()
        cursor.execute("select m.speciality,d.doctor_first_name,d.doctor_last_name,d.qualification,d.photo from  tbl_medical_speciality as m inner join   tbl_doctor as d on m.medical_speciality_id =d.medical_speciality_id")
        data=cursor.fetchall()
        return render(request,'Patient/index.html',{'data':data})
    else:
        return redirect('/index/')

def admin_logout(request):
    logout(request)
    request.session.delete()
    return redirect('/index/')

def user_logout(request):
    logout(request)
    request.session.delete()
    return redirect('/index/')

def hospital_action(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    data = {
       'username_exists':      Login.objects.filter(username=username).exists(),
        'error':"Username Already Exist"
    }
    if(data["username_exists"]==False):
        tbl1=Login()
        username=request.POST.get("username")
        tbl1.username=request.POST.get("username")
        password=request.POST.get("password")
        tbl1.password=request.POST.get("password")
        tbl1.Usertype="Hospital"
        tbl1.status="Not Approved"
        tbl1.save()
        obj=Login.objects.get(username=username,password=password)

        u=Hospital()
        u.login_id = obj.login_id
        u.hospital=request.POST.get("hospital")
        u.address =request.POST.get("address")
        u.email=request.POST.get("email")
        u.phone_number=request.POST.get("phone_number")
        u.district_id=request.POST.get("district")
        u.place=request.POST.get("place")

        u.save()
        messages.add_message(request, messages.INFO, 'Registered successfully.')
        return redirect('/hospital_registration/')
    else:
        messages.add_message(request, messages.INFO, 'Username already exist.. Try Again.')
        return redirect('/hospital_registration/')

def patient_action(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    data = {
       'username_exists':      Login.objects.filter(username=username).exists(),
        'error':"Username Already Exist"
    }
    if(data["username_exists"]==False):
        tbl1=Login()
        username=request.POST.get("username")
        tbl1.username=request.POST.get("username")
        password=request.POST.get("password")
        tbl1.password=request.POST.get("password")
        tbl1.Usertype="Patient"
        tbl1.status="Approved"
        tbl1.save()
        obj=Login.objects.get(username=username,password=password)

        u=Patients()
        u.login_id = obj.login_id
        u.patient_name=request.POST.get("patient_name")
        u.Address =request.POST.get("address")
        u.phone_number=request.POST.get("phone_number")
        u.district_id=request.POST.get("district")
        u.place=request.POST.get("place")
        u.dob=request.POST.get("dob")
        u.save()
        messages.add_message(request, messages.INFO, 'Registered successfully.')
        return redirect('/patient_registration/')
    else:
        messages.add_message(request, messages.INFO, 'Username already exist.. Try Again.')
        return redirect('/patient_registration/')

def display_district(request):
    state_id = request.GET.get("state_id")
    try:
        dist = District.objects.filter(state_id = state_id)
    except Exception as e:
        return JsonResponse({'error_message': str(e)}, status=400)
    return JsonResponse(list(dist.values('district_id', 'district')), safe = False)

def check_username(request):
    username = request.GET.get("username")
    data = {
       'username_exists':      Login.objects.filter(username=username).exists(),  # Corrected: Changed "login" to capitalized "Login"
        'error':"Username Already Exist"
    }
    if(data["username_exists"]==False):
        data["success"]="Available"

    return JsonResponse(data)

# Approval
def approve_hospital(request):
   if 'aname' in request.session:
        cursor=connection.cursor()
        cursor.execute("select p.*,s.state,d.district from  tbl_hospital as p inner join   tbl_district as d on p.district_id =d.district_id inner join tbl_state as s on d.state_id=s.state_id  where p.login_id in (select login_id from tbl_login where Usertype='Hospital' and status='Not Approved')")
        data=cursor.fetchall()
        return render(request,'Master/approve_hospital.html',{'data':data})
   else:
       return redirect('/index/')

def approve(request,id):
    if 'aname' in request.session:
        tbl=Login.objects.get(login_id=id)
        tbl.status="Approved"
        tbl.save()
        messages.add_message(request, messages.INFO, 'Updated successfully.')
        return redirect('/approve_hospital/')
    else:
       return redirect('/index/')

def reject(request,id):
    if 'aname' in request.session:
        tbl=Login.objects.get(login_id=id)
        tbl.status="Rejected"
        tbl.save()
        messages.add_message(request, messages.INFO, 'Rejected successfully.')
        return redirect('/approve_hospital/')
    else:
        return redirect('/login/')

def hospital_list(request):
   if 'aname' in request.session:
            cursor=connection.cursor()
            cursor.execute("select p.*,s.state,d.district from  tbl_hospital as p inner join   tbl_district as d on p.district_id =d.district_id inner join tbl_state as s on d.state_id=s.state_id  where p.login_id in (select login_id from tbl_login where Usertype='Hospital' and status='Approved')")
            data=cursor.fetchall()
            return render(request,'Master/approved_hospital.html',{'data':data})
   else:
        return redirect('/login/')
   
def Complaint_frm(request):
    if 'pname' in request.session:
        logid=request.session['slogid']
        data1 = Complaint.objects.filter(user_login_id=logid)
        return render(request,'Patient/complaint.html',{'data1':data1})
    else:
       return redirect('/index/')

def save_complaint(request):
    if 'pname' in request.session:
        tbl=Complaint()
        tbl.user_login_id=request.session['slogid']
        tbl.complaint=request.POST.get("complaint")
        tbl.reply="No"
        tbl.save()
        messages.add_message(request, messages.INFO, 'Added successfully.')
        return redirect('/add_complaint/')
    else:
       return redirect('/index/')

def delete_complaint(request,id):
    if 'pname' in request.session:
        tbl=Complaint.objects.get(complaint_id=id)
        tbl.delete()
        messages.add_message(request, messages.INFO, 'Deleted successfully.')
        return redirect('/add_complaint/')
    else:
       return redirect('/index/')

def feedback_frm(request):
    if 'pname' in request.session:
        logid=request.session['slogid']
        data1 = Feedback.objects.filter(user_login_id=logid)
        return render(request,'Patient/feedback.html',{'data1':data1})
    else:
       return redirect('/index/')

def save_feedback(request):
    if 'pname' in request.session:
        tbl=Feedback()
        tbl.user_login_id=request.session['slogid']
        tbl.feedback=request.POST.get("feedback")
        tbl.reply="No"
        tbl.save()
        messages.add_message(request, messages.INFO, 'Added successfully.')
        return redirect('/feedback/')
    else:
       return redirect('/index/')

def delete_feedback(request,id):
    if 'pname' in request.session:
        tbl=Feedback.objects.get(feedback_id=id)
        tbl.delete()
        messages.add_message(request, messages.INFO, 'Deleted successfully.')
        return redirect('/feedback/')
    else:
       return redirect('/index/')

# ----------------Admin Complaint -------------
def view_complaints(request):
    if 'aname' in request.session:
        cursor=connection.cursor()
        cursor.execute("select c.*,u.* from  tbl_complaint  as c inner join  tbl_patient as u  on c.user_login_id =u.login_id where c.reply='No'  order by c.complaint_id desc")
        data=cursor.fetchall()
        return render(request,'Master/view_complaints.html',{'data':data})
    else:
       return redirect('/index/')

def replied_list(request):
    if 'aname' in request.session:
        cursor=connection.cursor()
        cursor.execute("select c.*,u.* from  tbl_complaint  as c inner join  tbl_patient as u  on c.user_login_id =u.login_id where c.reply!='No' order by c.complaint_id desc")
        data=cursor.fetchall()
        return render(request,'Master/replied_complaints.html',{'data':data})
    else:
       return redirect('/index/')

def adm_reply_complaint(request,id):
    if 'aname' in request.session:
        return render(request,'Master/reply_complaint.html',{'id':id})
    else:
       return redirect('/index/')

def add_reply(request,id):
    tbl=Complaint.objects.get(complaint_id=id)
    tbl.reply=request.POST.get("reply")
    tbl.save()
    return redirect('/replied_list/')

# Admin feedback
def view_feedback(request):
    if 'aname' in request.session:
        cursor=connection.cursor()
        cursor.execute("select c.*,u.* from  tbl_feedback  as c inner join  tbl_patient as u  on c.user_login_id =u.login_id where c.reply='No'  order by c.feedback_id desc")
        data=cursor.fetchall()
        return render(request,'Master/view_feedback.html',{'data':data})
    else:
       return redirect('/index/')

def feedback_replied_list(request):
    if 'aname' in request.session:
        cursor=connection.cursor()
        cursor.execute("select c.*,u.* from  tbl_feedback  as c inner join  tbl_patient as u  on c.user_login_id =u.login_id where c.reply!='No' order by c.feedback_id desc")
        data=cursor.fetchall()
        return render(request,'Master/replied_feedback.html',{'data':data})
    else:
       return redirect('/index/')

def adm_reply_feedback(request,id):
    if 'aname' in request.session:
        return render(request,'Master/reply_feedback.html',{'id':id})
    else:
       return redirect('/index/')

def add_reply_feedback(request,id):
    tbl=Feedback.objects.get(feedback_id=id)
    tbl.reply=request.POST.get("reply")
    tbl.save()
    return redirect('/feedback_replied_list/')

#Doctor
def add_doctor(request):
    if 'aname' in request.session:
        data = State.objects.all()
        data2 = MedicalSpeciality.objects.all()
        return render(request,'Master/add_doctor.html',{'data':data,'data2':data2})
    else:
       return redirect('/login/')

def save_doctor(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    data = {
       'username_exists':      Login.objects.filter(username=username).exists(),
        'error':"Username Already Exist"
    }
    if(data["username_exists"]==False):
        tbl1=Login()
        tbl1.username=request.POST.get("username")
        tbl1.password=password
        tbl1.Usertype="Doctor"
        tbl1.status="Approved"
        tbl1.save()
        obj=Login.objects.get(username=username,password=password)

        u=Doctor()
        u.login_id = obj.login_id
       
        u.doctor_first_name=request.POST.get("doctor_first_name")
        u.doctor_last_name=request.POST.get("doctor_last_name")
        u.medical_speciality_id=request.POST.get("medical_speciality_id")
        u.address =request.POST.get("address")
        u.email=request.POST.get("email")
        u.phone_number=request.POST.get("phone_number")
        u.district_id=request.POST.get("district")
        u.place=request.POST.get("place")
        u.qualification=request.POST.get("qualification")
        photo=request.FILES['photo']
      
        split_tup = os.path.splitext(photo.name)
        file_extension = split_tup[1]
        
        dir_path = settings.MEDIA_ROOT
        count = 0
        for path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, path)):
                count += 1
        filecount=count+1
        filename=str(filecount)+file_extension
        obj=FileSystemStorage()
        file=obj.save(filename,photo)
        url1=obj.url(file)
        u.photo=url1
       
        u.save()
        messages.add_message(request, messages.INFO, 'Added successfully.')
        return redirect('/add_doctor/')
    else:
        messages.add_message(request, messages.INFO, 'Username already exist.. Try Again.')
        return redirect('/add_doctor/')

def doctor_list(request):
    if 'aname' in request.session:
            cursor=connection.cursor()
            cursor.execute("select p.*,s.state,d.district from  tbl_doctor as p inner join   tbl_district as d on p.district_id =d.district_id inner join tbl_state as s on d.state_id=s.state_id")
            data=cursor.fetchall()
            return render(request,'Master/doctor_list.html',{'data':data})
    else:
        return redirect('/login/')

def edit_doctor(request,id):
 if 'aname' in request.session:
    data=Doctor.objects.get(doctor_id=id)
    data1 = State.objects.all()
    data2 = MedicalSpeciality.objects.all()
    return render(request,'Master/edit_doctor.html',{'data':data,'data1':data1,'data2':data2})
 else:
      return redirect('/index/')

def update_doctor(request,id):
 if 'aname' in request.session:
    u=Doctor.objects.get(doctor_id=id)
    u.doctor_first_name=request.POST.get("doctor_first_name")
    u.doctor_last_name=request.POST.get("doctor_last_name")
    u.medical_speciality_id=request.POST.get("medical_speciality_id")
    u.address =request.POST.get("address")
    u.email=request.POST.get("email")
    u.phone_number=request.POST.get("phone_number")
    u.place=request.POST.get("place")
    u.qualification=request.POST.get("qualification")
    if len(request.FILES) != 0:
        photo=request.FILES['photo']

        split_tup = os.path.splitext(photo.name)
        file_extension = split_tup[1]
        
        dir_path = settings.MEDIA_ROOT
        count = 0
        for path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, path)):
                count += 1
        filecount=count+1
        filename=str(filecount)+file_extension
        obj=FileSystemStorage()
        file=obj.save(filename,photo)
        url1=obj.url(file)
        u.photo=url1
    u.save()
    messages.add_message(request, messages.INFO, 'Updated successfully.')
    return redirect('/doctor_list/')
 else:
      return redirect('/index/')

def delete_doctor(request,id):
 if 'aname' in request.session:
    tbl=Doctor.objects.get(doctor_id=id)
    logid=tbl.login_id
    tbl2=Login.objects.get(login_id=logid)
    tbl2.delete()
    tbl3=Doctor.objects.get(doctor_id=id)
    tbl3.delete()
    messages.add_message(request, messages.INFO, 'Deleted successfully.')
    return redirect('/doctor_list/')
 else:
      return redirect('/index/')
 
# Insurance
def add_insurance(request):
    if 'aname' in request.session:
        data = Insurance.objects.all()
        return render(request,'Master/add_insurance.html',{'data':data})
    else:
       return redirect('/index/')

def save_insurance(request):
    if 'aname' in request.session:
        c=request.POST.get("insurance_company")  # Corrected: Typo "insuarnce_company" aligned to "insurance_company"
     
        data = {
          'exists':      Insurance.objects.filter(insuarnce_company=c).exists(),
          'error':"Already Exist"
        }
        if(data["exists"]==False):  
            u=Insurance()
            u.insuarnce_company=request.POST.get("insurance_company")    
            u.description=request.POST.get("description")          
            u.save()
            messages.add_message(request, messages.INFO, 'Added successfully.')
            return redirect('/add_insurance/')
        else:
           messages.add_message(request, messages.INFO, 'Failed..  insurance has been already added ')
           return redirect('/add_insurance/')
    else:
       return redirect('/index/')

def edit_insurance(request,id):
 if 'aname' in request.session:
    data=Insurance.objects.get(insurance_id=id)
    return render(request,'Master/edit_insurance.html',{'data':data})
 else:
      return redirect('/index/')

def update_insurance(request,id):
 if 'aname' in request.session:
    u=Insurance.objects.get(insurance_id=id)
    u.insuarnce_company=request.POST.get("insurance_company")    
    u.description=request.POST.get("description")      
    u.save()
    messages.add_message(request, messages.INFO, 'Updated successfully.')
    return redirect('/add_insurance/')
 else:
      return redirect('/index/')

def delete_insurance(request,id):
 if 'aname' in request.session:
    tbl=Insurance.objects.get(insurance_id=id)
    tbl.delete()
    messages.add_message(request, messages.INFO, 'Deleted successfully.')
    return redirect('/add_insurance/')
 else:
      return redirect('/index/')
 
def appointment(request):
    if 'pname' in request.session:
        data = MedicalSpeciality.objects.all()
        return render(request,'Patient/appointment.html',{'data':data})
    else:
        return redirect('/index/')

def display_speciality(request):
        cursor=connection.cursor()
        cursor.execute("select m.medical_speciality_id,m.speciality from  tbl_medical_speciality as m inner join   tbl_doctor as d on m.medical_speciality_id =d.medical_speciality_id inner join tbl_hospital as h on h.login_id=d.hospital_login_id")
        data=cursor.fetchall()
        str1='<option value="">--Select--</option>'  # Corrected: Swapped double quotes for single quotes to resolve SyntaxError
        for k in data:
            str1+="<option value="+str(k[0])+">"+str(k[1])+"</option>"        
        return HttpResponse(str1)

def display_doctor(request):
    medical_speciality_id = request.GET.get("medical_speciality_id")
    try:
        dist = Doctor.objects.filter(medical_speciality_id = medical_speciality_id)
    except Exception as e:
        return JsonResponse({'error_message': str(e)}, status=400)
    return JsonResponse(list(dist.values('login_id', 'doctor_first_name', 'doctor_last_name')), safe = False)

def save_appointment(request):
    if 'pname' in request.session:
        u=Appointment()
        logid=  request.session['slogid']
        u.patient_login_id = logid
        u.doctor_login_id=request.POST.get("doctor")    
        u.appointment_date=request.POST.get("appointment_date")          
        u.save()
        messages.add_message(request, messages.INFO, 'Added successfully.')
        return redirect('/appointment/')
    else:
       return redirect('/index/')

def history(request):
    if 'pname' in request.session:
        logid=  request.session['slogid']
        cursor=connection.cursor()
        cursor.execute("select  a.appointment_date,a.entry_date,d.doctor_first_name,d.doctor_last_name,m.speciality,a.appointment_id from tbl_appointment as a inner join   tbl_doctor as d on a.doctor_login_id =d.login_id  inner join tbl_medical_speciality as m  on m.medical_speciality_id=d.medical_speciality_id   where a.patient_login_id="+str(logid))
        data=cursor.fetchall()
        return render(request,'Patient/appointment_list.html',{'data':data})
    else:
        return redirect('/index/')

def display_hospital_list(request):
        district_id = request.GET.get("district_id")
        cursor=connection.cursor()
        cursor.execute("select h.* from  tbl_hospital as h inner join tbl_login as l on h.login_id=l.login_id where district_id="+str(district_id)+" and l.status='Approved'")
        data=cursor.fetchall()
        str1="<table class='table table-bordered'>  <thead><th>Id</th><th>Hospital</th><th>Address</th><th>Email</th><th>Phone Number</th><th>Place</th></thead>"
        count=1
        for k in data:
            str1+="<tr><td>"+str(count)+"<td>"+str(k[2])+"</td><td>"+str(k[3])+"</td><td>"+str(k[4])+"</td><td>"+str(k[5])+"</td><td>"+str(k[7])+"</td><td><a href='/doctors/"+str(k[1])+"' class='btn btn-info'>Doctors</a></td>"
            count=count+1
        str1+="</table>"                
        return HttpResponse(str1)

def doctors(request, id):
    if 'pname' in request.session:
        cursor = connection.cursor()
        query = """
            SELECT d.*, h.*
            FROM tbl_doctor AS d
            INNER JOIN tbl_medical_speciality AS h
                ON h.medical_speciality_id = d.medical_speciality_id
            WHERE d.hospital_login_id = %s
        """
        cursor.execute(query, [id])
        data1 = cursor.fetchall()
        return render(request, 'Patient/doctors.html', {'data1': data1})
    else:
        return redirect('/index/')

def insurance(request,id):
    if 'pname' in request.session:
        data = Insurance.objects.all()
        return render(request,'Patient/insurance.html',{'data':data})
    else:
        return redirect('/index/')

def patient_profile(request):
    if 'pname' in request.session:
        logid=  request.session['slogid']
        data = Patients.objects.get(login_id =logid)
        return render(request,'Patient/profile.html',{'data':data})
    else:
        return redirect('/index/')

def update_profile(request,id):
    u=Patients.objects.get(patient_id=id)
    u.patient_name=request.POST.get("patient_name")
    u.Address =request.POST.get("address")
    u.phone_number=request.POST.get("phone_number")
    u.place=request.POST.get("place")
    u.dob=request.POST.get("dob") 
    u.save()
    messages.add_message(request, messages.INFO, 'Updated successfully.')
    return redirect('/patient_profile/')

def patient_change_password(request):
    if 'pname' in request.session:
        return render(request,'Patient/change_password.html')
    else:
       return redirect('/index/')

def update_password(request):
    if 'pname' in request.session:
        id=request.session['slogid']
        opass=request.POST.get("opassword")
        npass=request.POST.get("password")
        obj1=Login.objects.filter(login_id=id,password=opass)
        if(obj1):
            tbl1=Login.objects.get(login_id=id)
            tbl1.password=npass
            tbl1.save()
            messages.add_message(request, messages.INFO, 'Updated Please Login Using new Password.')
            return redirect('/login/')
        else:
            messages.add_message(request, messages.INFO, 'Invalid Data')
            return redirect('/patient_change_password/')
    else:
       return redirect('/index/')

def patient_list(request):
    if 'aname' in request.session:
        cursor=connection.cursor()
        cursor.execute("select distinct p.* from tbl_appointment as a inner join   tbl_doctor as d on a.doctor_login_id =d.login_id  inner join tbl_medical_speciality as m  on m.medical_speciality_id=d.medical_speciality_id inner join tbl_patient as p on p.login_id=a.patient_login_id")
        data=cursor.fetchall()
        likm={}
        for i in data:
           d = i[7]
           id=i[0]
           y=d.strftime("%Y")
           m=d.strftime("%m")
           day=d.strftime("%d")        
           age =calculate_age(int(day),int(m),int(y))
           likm[id]=age
        return render(request,'Master/patient_list.html',{'data':data,'likm':likm})
    else:
       return redirect('/index/')

def calculate_age(day, month, year):
    today = date.today()
    birthdate = date(year, month, day)
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

def appointment_list(request):
    if 'aname' in request.session:
        today = date.today()  # Corrected: date.today() used securely via imported module
        cursor=connection.cursor()
        cursor.execute("select  p.*,d.doctor_first_name,d.doctor_last_name,d.photo,m.speciality,a.appointment_date from tbl_appointment as a inner join   tbl_doctor as d on a.doctor_login_id =d.login_id  inner join tbl_medical_speciality as m  on m.medical_speciality_id=d.medical_speciality_id inner join tbl_patient as p on p.login_id=a.patient_login_id   where  a.appointment_date>='"+str(today)+"'")
        data=cursor.fetchall()
        likm={}
        for i in data:
           d = i[7]
           id=i[0]
           y=d.strftime("%Y")
           m=d.strftime("%m")
           day=d.strftime("%d")        
           age =calculate_age(int(day),int(m),int(y))
           likm[id]=age
        return render(request,'Master/appointment_list.html',{'data':data,'likm':likm})
    else:
       return redirect('/index/')

def appointment_approval(request):
    if 'dname' in request.session:
        today = date.today()  # Corrected: date.today() used securely via imported module
        logid=request.session['slogid']
        cursor=connection.cursor()
        query="select p.*,d.doctor_first_name,d.doctor_last_name,d.photo,m.speciality,a.appointment_date, a.appointment_id from tbl_appointment as a inner join   tbl_doctor as d on a.doctor_login_id =d.login_id  inner join tbl_medical_speciality as m  on m.medical_speciality_id=d.medical_speciality_id inner join tbl_patient as p on p.login_id=a.patient_login_id   where a.status='Not Consulted' and  a.doctor_login_id="+str(logid)+" and a.appointment_date<='"+str(today)+"'"
        cursor.execute(query)
        data=cursor.fetchall()
        likm={}
        for i in data:
           d = i[7]
           id=i[0]
           y=d.strftime("%Y")
           m=d.strftime("%m")
           day=d.strftime("%d")        
           age =calculate_age(int(day),int(m),int(y))
           likm[id]=age
        return render(request,'Doctor/appointment_approval.html',{'data':data,'likm':likm})
    else:
       return redirect('/index/')

def new_appointment(request):
    if 'dname' in request.session:
        today = date.today()  # Corrected: date.today() used securely via imported module
        logid=request.session['slogid']
        cursor=connection.cursor()
        query="select p.*,d.doctor_first_name,d.doctor_last_name,d.photo,m.speciality,a.appointment_date, a.appointment_id from tbl_appointment as a inner join   tbl_doctor as d on a.doctor_login_id =d.login_id  inner join tbl_medical_speciality as m  on m.medical_speciality_id=d.medical_speciality_id inner join tbl_patient as p on p.login_id=a.patient_login_id   where a.status='Accepted' and  a.doctor_login_id="+str(logid)+" and a.appointment_date='"+str(today)+"'"
        cursor.execute(query)
        data=cursor.fetchall()
        likm={}
        for i in data:
           d = i[7]
           id=i[0]
           y=d.strftime("%Y")
           m=d.strftime("%m")
           day=d.strftime("%d")        
           age =calculate_age(int(day),int(m),int(y))
           likm[id]=age
        return render(request,'Doctor/appointment_list.html',{'data':data,'likm':likm})
    else:
       return redirect('/index/')

def add_prescription(request,id):
    if 'dname' in request.session:
        data = Lab.objects.all()
        return render(request,'Doctor/add_prescription.html',{'id':id,'data':data})
    else:
       return redirect('/index/')

def save_prescription(request,id):
    if 'dname' in request.session:
        tbl=prescription()
        tbl.appointment_id=id
        tbl.visiting_date=request.POST.get("visiting_date")
        tbl.symptoms=request.POST.get("symptoms")
        tbl.medicine=request.POST.get("medicine")
        tbl.uses=request.POST.get("uses")
        tbl.details=request.POST.get("details")
        tbl.save()
     
        li=request.POST.getlist("test_type")
        for i in li:
            tbl2=lab_test()
            tbl2.appointment_id=id
            tbl2.test_id=i
            tbl2.save()

        tbl1=Appointment.objects.get(appointment_id=id)
        tbl1.status="Consulted"
        tbl1.save()
        messages.add_message(request, messages.INFO, 'Added successfully.')
        return redirect('/new_appointment/')
    else:
       return redirect('/index/')

def all_appointment_list(request):
    if 'dname' in request.session:
        logid=request.session['slogid']
        cursor=connection.cursor()
        query="select  p.*,d.doctor_first_name,d.doctor_last_name,d.photo,m.speciality,a.appointment_date,a.appointment_id from tbl_appointment as a inner join   tbl_doctor as d on a.doctor_login_id =d.login_id  inner join tbl_medical_speciality as m  on m.medical_speciality_id=d.medical_speciality_id inner join tbl_patient as p on p.login_id=a.patient_login_id   where a.status='Consulted' and  a.doctor_login_id="+str(logid)
        cursor.execute(query)
        data=cursor.fetchall()
        likm={}
        for i in data:
           d = i[7]
           id=i[0]
           y=d.strftime("%Y")
           m=d.strftime("%m")
           day=d.strftime("%d")        
           age =calculate_age(int(day),int(m),int(y))
           likm[id]=age
        return render(request,'Doctor/all_appointment_list.html',{'data':data,'likm':likm})
    else:
       return redirect('/index/')

def view_prescription(request,id):
    if 'dname' in request.session:
        cursor=connection.cursor()
        query="select  * from tbl_prescription  where  appointment_id="+str(id)
        cursor.execute(query)
        data=cursor.fetchall()

        query="select  * from tbl_lab_test inner join tbl_lab_test_type on tbl_lab_test.test_id=tbl_lab_test_type.lab_test_type_id inner join  tbl_lab on tbl_lab.login_id=tbl_lab_test_type.lab_login_id   where  appointment_id="+str(id)
        cursor.execute(query)
        data2=cursor.fetchall()

        return render(request,'Doctor/view_prescription.html',{'data':data,'data2':data2})
    else:
       return redirect('/index/')

def dr_view_patient(request):
    if 'dname' in request.session:
        logid=request.session['slogid']
        cursor=connection.cursor()
        query="select distinct p.*,di.district,s.state from tbl_appointment as a inner join   tbl_doctor as d on a.doctor_login_id =d.login_id  inner join tbl_medical_speciality as m  on m.medical_speciality_id=d.medical_speciality_id inner join tbl_patient as p on p.login_id=a.patient_login_id inner join tbl_district as di on p.district_id=di.district_id inner join tbl_state as s on s.state_id=di.state_id   where a.status='Consulted' and  a.doctor_login_id="+str(logid)
        cursor.execute(query)
        data=cursor.fetchall()
        likm={}
        for i in data:
           d = i[7]
           id=i[0]
           y=d.strftime("%Y")
           m=d.strftime("%m")
           day=d.strftime("%d")        
           age =calculate_age(int(day),int(m),int(y))
           likm[id]=age
        return render(request,'Doctor/view_patient.html',{'data':data,'likm':likm})
    else:
       return redirect('/index/')

def dr_view_patient_records(request,id):
    if 'dname' in request.session:
        cursor=connection.cursor()
        query="select  * from tbl_prescription as p inner join tbl_appointment as a on p.appointment_id=a.appointment_id  where  a.patient_login_id="+str(id)
        cursor.execute(query)
        data=cursor.fetchall()
        query="select  * from tbl_lab_test inner join tbl_lab_test_type on tbl_lab_test.test_id=tbl_lab_test_type.lab_test_type_id inner join  tbl_lab on tbl_lab.login_id=tbl_lab_test_type.lab_login_id inner join tbl_appointment  on tbl_appointment.appointment_id=tbl_lab_test.appointment_id   where  tbl_appointment.patient_login_id="+str(id)
        cursor.execute(query)
        data2=cursor.fetchall()
        return render(request,'Doctor/view_patient_records.html',{'data':data,'data2':data2})
    else:
       return redirect('/index/')

# Doctor Profile
def doctor_profile(request):
    if 'dname' in request.session:
        logid=  request.session['slogid']
        data = Doctor.objects.get(login_id =logid)
        data1 = State.objects.all()
        data2 = MedicalSpeciality.objects.all()
        return render(request,'Doctor/profile.html',{'data':data,'data1':data1,'data2':data2})
    else:
        return redirect('/index/')

def update_dr_profile(request,id):
    if 'dname' in request.session:
        u=Doctor.objects.get(doctor_id=id)
        u.doctor_first_name=request.POST.get("doctor_first_name")
        u.doctor_last_name=request.POST.get("doctor_last_name")
        u.address =request.POST.get("address")
        u.email=request.POST.get("email")
        u.phone_number=request.POST.get("phone_number")
        u.place=request.POST.get("place")
        u.qualification=request.POST.get("qualification")
        if len(request.FILES) != 0:
            photo=request.FILES['photo']
            split_tup = os.path.splitext(photo.name)
            file_extension = split_tup[1]
            dir_path = settings.MEDIA_ROOT
            count = 0
            for path in os.listdir(dir_path):
                if os.path.isfile(os.path.join(dir_path, path)):
                    count += 1
            filecount=count+1
            filename=str(filecount)+file_extension
            obj=FileSystemStorage()
            file=obj.save(filename,photo)
            url1=obj.url(file)
            u.photo=url1
        u.save()
        messages.add_message(request, messages.INFO, 'Updated successfully.')
        return redirect('/doctor_profile/')
    else:
      return redirect('/index/')

def change_password_doctor(request):
    if 'dname' in request.session:
        return render(request,'Doctor/change_password.html')
    else:
       return redirect('/index/')

def update_dr_password(request):
    if 'dname' in request.session:
        id=request.session['slogid']
        opass=request.POST.get("opassword")
        npass=request.POST.get("password")
        obj1=Login.objects.filter(login_id=id,password=opass)
        if(obj1):
            tbl1=Login.objects.get(login_id=id)
            tbl1.password=npass
            tbl1.save()
            messages.add_message(request, messages.INFO, 'Updated Please Login Using new Password.')
            return redirect('/login/')
        else:
            messages.add_message(request, messages.INFO, 'Invalid Data')
            return redirect('/change_password_doctor/')
    else:
       return redirect('/index/')

# Speciality
def save_speciality(request):
    if 'aname' in request.session:
        tbl=MedicalSpeciality()
        tbl.speciality=request.POST.get("category")
        tbl.save()
        messages.add_message(request, messages.INFO, 'Added successfully.')
        return redirect('/add_speciality/')
    else:
        return redirect('/login/')

def add_speciality(request):
 if 'aname' in request.session:
    data=MedicalSpeciality.objects.all()
    return render(request,'Master/speciality.html',{'data':data})
 else:
      return redirect('/index/')

def edit_speciality(request,id):
 if 'aname' in request.session:
    data=MedicalSpeciality.objects.get(medical_speciality_id=id)
    return render(request,'Master/edit_speciality.html',{'data':data})
 else:
      return redirect('/index/')

def update_speciality(request,id):
 if 'aname' in request.session:
    tbl=MedicalSpeciality.objects.get(medical_speciality_id=id)
    tbl.speciality=request.POST.get("category")
    tbl.save()
    messages.add_message(request, messages.INFO, 'Updated successfully.')
    return redirect('/add_speciality/')
 else:
      return redirect('/index/')

def delete_speciality(request,id):
 if 'aname' in request.session:
    tbl=MedicalSpeciality.objects.get(medical_speciality_id=id)
    tbl.delete()
    messages.add_message(request, messages.INFO, 'Deleted successfully.')
    return redirect('/add_speciality/')
 else:
      return redirect('/index/')
 
def view_prescription_patient(request,id):
    if 'pname' in request.session:
        cursor=connection.cursor()
        query="select  * from tbl_prescription  where  appointment_id="+str(id)
        cursor.execute(query)
        data=cursor.fetchall()

        query="select  tbl_lab_test.*,tbl_lab_test_type.*,tbl_lab.* from tbl_lab_test inner join tbl_lab_test_type on tbl_lab_test.test_id=tbl_lab_test_type.lab_test_type_id inner join  tbl_lab on tbl_lab.login_id=tbl_lab_test_type.lab_login_id   where  appointment_id="+str(id)
        cursor.execute(query)
        data2=cursor.fetchall()
        return render(request,'patient/view_prescription.html',{'data':data,'data2':data2})
    else:
       return redirect('/index/')

# Lab
def add_lab(request):
    if 'aname' in request.session:
        return render(request,'Master/add_lab.html')
    else:
       return redirect('/login/')

def save_lab(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    data = {
       'username_exists':      Login.objects.filter(username=username).exists(),
        'error':"Username Already Exist"
    }
    if(data["username_exists"]==False):
        tbl1=Login()
        tbl1.username=request.POST.get("username")
        tbl1.password=password
        tbl1.Usertype="Lab"
        tbl1.status="Approved"
        tbl1.save()
        obj=Login.objects.get(username=username,password=password)

        u=Lab()
        u.login_id = obj.login_id
        u.name=request.POST.get("name")
        u.address =request.POST.get("address")
        u.email=request.POST.get("email")
        u.phone_number=request.POST.get("phone_number")
        u.place=request.POST.get("place")  
        u.save()
        messages.add_message(request, messages.INFO, 'Added successfully.')
        return redirect('/add_lab/')
    else:
        messages.add_message(request, messages.INFO, 'Username already exist.. Try Again.')
        return redirect('/add_lab/')

def lab_details(request):
    if 'aname' in request.session:
            data=Lab.objects.all()
            return render(request,'Master/lab_details.html',{'data':data})
    else:
        return redirect('/login/')

def edit_lab(request,id):
 if 'aname' in request.session:
    data=Lab.objects.get(lab_id=id)
    return render(request,'Master/edit_lab.html',{'data':data})
 else:
      return redirect('/index/')

def update_lab(request,id):
 if 'aname' in request.session:
    u=Lab.objects.get(lab_id=id)
    u.name=request.POST.get("name")
    u.address =request.POST.get("address")
    u.email=request.POST.get("email")
    u.phone_number=request.POST.get("phone_number")
    u.place=request.POST.get("place")  
    u.save()
    messages.add_message(request, messages.INFO, 'Updated successfully.')
    return redirect('/lab_details/')
 else:
      return redirect('/index/')

def delete_lab(request,id):
 if 'aname' in request.session:
    tbl=Lab.objects.get(lab_id=id)
    logid=tbl.login_id
    tbl2=Login.objects.get(login_id=logid)
    tbl2.delete()
    tbl3=Lab.objects.get(lab_id=id)
    tbl3.delete()
    messages.add_message(request, messages.INFO, 'Deleted successfully.')
    return redirect('/lab_details/')
 else:
      return redirect('/index/')

def save_test_type(request):
    if 'lname' in request.session:
        id=request.session['slogid']
        tbl=lab_test_type()
        tbl.tests=request.POST.get("test_type")
        tbl.lab_login_id=id
        tbl.save()
        messages.add_message(request, messages.INFO, 'Added successfully.')
        return redirect('/add_test_type/')
    else:
        return redirect('/login/')

def add_test_type(request):
 if 'lname' in request.session:
    id=request.session['slogid']
    data=lab_test_type.objects.filter(lab_login_id=id)
    return render(request,'Lab/add_test_type.html',{'data':data})
 else:
      return redirect('/index/')

def edit_test_type(request,id):
 if 'lname' in request.session:
    data=lab_test_type.objects.get(lab_test_type_id=id)
    return render(request,'Lab/edit_test_type.html',{'data':data})
 else:
      return redirect('/index/')

def update_test_type(request,id):
 if 'lname' in request.session:
    tbl=lab_test_type.objects.get(lab_test_type_id=id)
    tbl.tests=request.POST.get("test_type")
    tbl.save()
    messages.add_message(request, messages.INFO, 'Updated successfully.')
    return redirect('/add_test_type/')
 else:
      return redirect('/index/')

def delete_test_type(request,id):
 if 'lname' in request.session:
    tbl=lab_test_type.objects.get(lab_test_type_id=id)
    tbl.delete()
    messages.add_message(request, messages.INFO, 'Deleted successfully.')
    return redirect('/add_test_type/')
 else:
      return redirect('/index/')

def display_lab_type(request):
    lab_id = request.GET.get("lab_login_id")
    try:
        dist = lab_test_type.objects.filter(lab_login_id = lab_id)
    except Exception as e:
        return JsonResponse({'error_message': str(e)}, status=400)
    return JsonResponse(list(dist.values('lab_test_type_id', 'tests')), safe = False)

def view_test_list(request):
    if 'lname' in request.session:
        login_id = request.session['slogid']
        cursor = connection.cursor()

        query = """
        SELECT *
        FROM tbl_lab_test
        INNER JOIN tbl_lab_test_type
            ON tbl_lab_test.test_id = tbl_lab_test_type.lab_test_type_id
        INNER JOIN tbl_lab
            ON tbl_lab.login_id = tbl_lab_test_type.lab_login_id
        INNER JOIN tbl_appointment
            ON tbl_appointment.appointment_id = tbl_lab_test.appointment_id
        INNER JOIN tbl_patient
            ON tbl_appointment.patient_login_id = tbl_patient.login_id
        WHERE tbl_lab_test.status='Result is not Prepared'
        AND tbl_lab.login_id=%s
        """

        cursor.execute(query, [login_id])
        data = cursor.fetchall()
        likm = {}

        for row in data:
            dob = row[30]
            if isinstance(dob, str):
                try:
                    dob = datetime.strptime(dob, "%Y-%m-%d").date()  # Corrected: Utilized full module datetime path
                except ValueError:
                    continue

            patient_age = calculate_age(
                dob.day,
                dob.month,
                dob.year
            )
            likm[row[0]] = patient_age

        return render(
            request,
            'Lab/view_test_list.html',
            {'data': data, 'likm': likm}
        )

    return redirect('/index/')

def add_test_result(request, id):
    if 'lname' in request.session:
        return render(
            request,
            'Lab/add_test_result.html',
            {'id': id}
        )
    return redirect('/index/')

def save_test_result(request, id):
    if 'lname' in request.session:
        tbl = lab_test.objects.get(lab_test_id=id)
        tbl.description = request.POST.get("description")
        tbl.status = "Result is prepared"
        result = request.FILES.get('result')
        if not result:
            messages.error(request, 'Please upload the test result.')
            return redirect('/add_test_result/' + str(id) + '/')

        split_tup = os.path.splitext(result.name)
        file_extension = split_tup[1].replace(".", "")
        dir_path = settings.MEDIA_ROOT
        count = 0

        for path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, path)):
                count += 1

        filecount = count + 1
        filename = str(filecount) + "." + file_extension
        obj = FileSystemStorage()
        file = obj.save(filename, result)
        url1 = obj.url(file)
        tbl.result = url1
        tbl.save()

        messages.add_message(
            request,
            messages.INFO,
            'Added successfully.'
        )
        return redirect('/view_test_list/')

    return redirect('/login/')

def view_test_result(request):
    if 'lname' in request.session:
        login_id = request.session['slogid']
        cursor = connection.cursor()

        query = """
        SELECT *
        FROM tbl_lab_test
        INNER JOIN tbl_lab_test_type
            ON tbl_lab_test.test_id = tbl_lab_test_type.lab_test_type_id
        INNER JOIN tbl_lab
            ON tbl_lab.login_id = tbl_lab_test_type.lab_login_id
        INNER JOIN tbl_appointment
            ON tbl_appointment.appointment_id = tbl_lab_test.appointment_id
        INNER JOIN tbl_patient
            ON tbl_appointment.patient_login_id = tbl_patient.login_id
        WHERE tbl_lab_test.status='Result is prepared'
        AND tbl_lab.login_id=%s
        """

        cursor.execute(query, [login_id])
        data = cursor.fetchall()
        likm = {}

        for row in data:
            dob = row[30]
            if isinstance(dob, str):
                try:
                    # Corrected: Utilized full module datetime path
                    dob = datetime.strptime(dob, "%Y-%m-%d").date()
                except ValueError:
                    continue

            patient_age = calculate_age(
                dob.day,
                dob.month,
                dob.year
            )
            likm[row[0]] = patient_age

        return render(
            request,
            'Lab/view_test_result.html',
            {'data': data, 'likm': likm}
        )

    return redirect('/index/')
    
def approve_appointment(request,id):
    if 'dname' in request.session:
        tbl=Appointment.objects.get(appointment_id=id)
        tbl.status="Accepted"
        tbl.save()
        messages.add_message(request, messages.INFO, 'Accepted successfully.')
        return redirect('/appointment_approval/')
    else:
       return redirect('/index/')

def reject_appointment(request,id):
    if 'dname' in request.session:
        tbl=Appointment.objects.get(appointment_id=id)
        tbl.status="Rejected"
        tbl.save()
        messages.add_message(request, messages.INFO, 'Rejected successfully.')
        return redirect('/appointment_approval/')
    else:
        return redirect('/login/')

def appointment_status(request):
    if 'pname' in request.session:
        logid=  request.session['slogid']
        cursor=connection.cursor()
        cursor.execute("select  a.appointment_date,a.entry_date,d.doctor_first_name,d.doctor_last_name,m.speciality,a.appointment_id, a.status from tbl_appointment as a inner join   tbl_doctor as d on a.doctor_login_id =d.login_id  inner join tbl_medical_speciality as m  on m.medical_speciality_id=d.medical_speciality_id   where a.patient_login_id="+str(logid))
        data=cursor.fetchall()
        return render(request,'Patient/appointment_status.html',{'data':data})
    else:
        return redirect('/index/')