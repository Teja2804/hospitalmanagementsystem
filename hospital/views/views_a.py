from django.shortcuts import render, redirect
from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.db import connection
from django.contrib import messages
import sys
import base64
from datetime import datetime
from datetime import date
from django.http import HttpResponse
from django.template.loader import get_template
import smtplib
from django.utils.datastructures import MultiValueDictKeyError

def userpage(request):
    return render(request, 'web_app/userpage.html')

def homeuser(request):
    return render(request, 'web_app/homeuser.html')

def userlog(request):
    return render(request, 'web_app/userlog.html')

def register(request):
    return render(request, 'web_app/register.html')

def vaccineapp(request):
    return render(request, 'web_app/vaccineapp.html')

def doctorapp(request):
    return render(request, 'web_app/doctorapp.html')

def appointmentfordiagnosis(request):
    return render(request, 'web_app/appointmentfordiagnosis.html')

def bp_d(request):
    return render(request, 'web_app/bpapp.html')

def diabetes_d(request):
    return render(request, 'web_app/diabetesapp.html')

def request_c(request):
    return render(request, 'web_app/request_c.html')

def userloginfill(request):
    if request.method=='GET':
        email = request.GET["useremail"]
        passw = request.GET["password"]
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users WHERE email=%s AND password=%s AND role='patient'""",(email,passw))       
        row = cursor.fetchall()
        users=[]
        data={
            'users':None
        }
        a = cursor.rowcount
        if a!=0:
           return render(request,'web_app/userbase.html')
        else:
             messages.success(request,'enter correct credentials!!')
             return render(request, 'web_app/register.html')

def userregister(request):
    if request.method=='GET':
        username = request.GET["username"]
        usernumb = request.GET["mobilenum"]
        add = request.GET["address"]
        email = request.GET["useremail"]
        passw = request.GET["password"]
        cursor = connection.cursor()
        
        # print(username, usernumb, add, email, passw, cursor)
        
        try:    
                cursor.execute("""SELECT * FROM users WHERE email=%s AND role='patient'""",[email])   
                row = cursor.fetchall()
                users=[]
                data={
                'users':None
                }
                a = cursor.rowcount
                if a!=0:    
                  return render(request,'web_app/userlog.html')
                else:
                 cursor.execute("""select max(userid) from users""")  
                 uid=cursor.fetchone()
                 cursor.execute("""INSERT INTO users VALUES (%s,%s,%s,%s,%s,%s,%s)""",(uid[0] + 1,username,usernumb,add,'patient',passw,email))      
                 return render(request, 'web_app/userlog.html')
        finally:
            cursor.close()            

def ViewDoctorProfile(request):    
        cursor = connection.cursor()
        cursor.execute("""SELECT  * FROM doctors""")
        print(cursor.rowcount) 
        row = cursor.fetchall()
        doctors=[]
        data ={
            'doctors':None
        }
        a = cursor.rowcount
        if a!=0:
            for n in range(a):
                doctors.append({
                    'did':row[n][0],
                    'dname':row[n][1],
                    'specialisation':row[n][2],
                    'available_from':row[n][3],
                    'available_to':row[n][4],
                })
            data = {
                'doctors':doctors,
            }         
        return render(request, 'web_app/ViewDoctorProfile.html',data)

def Medicines(request):
    cursor = connection.cursor()
    cursor.execute("""SELECT  * FROM medicines""")
    print(cursor.rowcount) 
    row = cursor.fetchall()
    medicines=[]
    data ={
        'medicimes':None
    }
    a = cursor.rowcount
    if a!=0:
        for n in range(a):
            medicines.append({
                'medicine_id':row[n][0],
                'medicine_name':row[n][1],
                'stock_left':row[n][2],
                'last_updates':row[n][3],
            })
        data = {
            'medicines':medicines,
        }         
    return render(request, 'web_app/Medicines.html',data)

def diabetes(request):
    if request.method == 'GET':
        val = request.GET.get('userid',None)
        cursor = connection.cursor()
        cursor.execute("""SELECT  * FROM users where userid = %s""",[val])
        print(cursor.rowcount) 
        row = cursor.fetchall()
        diabetes=[]
        data ={
            'diabetes':None
        }
        a = cursor.rowcount
        if a!=0:
            for n in range(a):
                diabetes.append({
                    'uid':row[n][0],
                    'testid':row[n][1],
                    'sugar_level':row[n][2],
                    'ppsl':row[n][3],
                    'insulin_level':row[n][4],
                    'test_date':row[n][5],
                })
            data = {
                'diabetes':diabetes,
            }         
        return render(request, 'web_app/diabetes.html',data)

def bp(request):
    if request.method == 'GET':
        val = request.GET.get('userid',None)
        cursor = connection.cursor()
        cursor.execute("""SELECT  * FROM users where userid = %s""",[val])
        print(cursor.rowcount) 
        row = cursor.fetchall()
        bp=[]
        data ={
            'bp':None
        }
        a = cursor.rowcount
        if a!=0:
            for n in range(a):
                bp.append({
                    'uid':row[n][0],
                    'testid':row[n][1],
                    'systolic_pressure':row[n][2],
                    'diastolic_pressure':row[n][3],
                    'test_date':row[n][4],
                })
            data = {
                'bp':bp,
            }         
        return render(request, 'web_app/bp.html',data)

def vaccinefill(request):
    if request.method=='GET':
        user_id = request.GET["uid"]
        appdate = request.GET["appointment_date"]
        cursor = connection.cursor()
        try:
             cursor.execute("""SELECT * FROM users WHERE userid=%s """,[user_id])       
             row = cursor.fetchall()
             a = cursor.rowcount
             if a!=0:
               cursor.execute("""SELECT * FROM vaccine WHERE appointment_date=%s """,[appdate])       
               row = cursor.fetchall()
               b = cursor.rowcount
               if b<100:
                cursor.execute("""INSERT INTO vaccine VALUES (%s,%s)""",(user_id,appdate)) 
                  
                return render(request, 'web_app/successful.html')
               else: 
                    return render(request, 'web_app/notsuccessful.html')
             else:
                 messages.success(request,'Enter correct credentials!!')
                 return render(request, 'web_app/vaccineapp.html')    
        finally:
            cursor.close()     
    
def doctorfill(request):
    if request.method=='GET':
        user_id = request.GET["uid"]
        doc_id = request.GET.get('docid',None)
        appdate = request.GET["appointment_date"]
        cursor = connection.cursor()
        try:
             cursor.execute("""SELECT * FROM users WHERE userid=%s """,[user_id])       
             row = cursor.fetchall()
             a = cursor.rowcount
             if a!=0:
               cursor.execute("""SELECT * FROM doctorappointments WHERE appointment_date=%s """,[appdate])       
               row = cursor.fetchall()
               b = cursor.rowcount
               if b<10:
                cursor.execute("""INSERT INTO doctorappointments VALUES (%s,%s,%s)""",(user_id,doc_id,appdate)) 
                  
                return render(request, 'web_app/successful.html')
               else: 
                    return render(request, 'web_app/notsuccessful.html')
             else:
                 messages.success(request,'Enter correct credentials!!')
                 return render(request, 'web_app/doctorapp.html')    
        finally:
            cursor.close()

def patientprofileinfo(request):
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM users WHERE userid='1' AND role='patient'""")    
    print(cursor.rowcount) 
    row = cursor.fetchall()
    users=[]
    data ={
        'users':None
    }
    a = cursor.rowcount
    if a!=0:
        for n in range(a):
            users.append({
                'userid':row[n][0],
                'username':row[n][1],
                'mobilenum':row[n][2],
                'address':row[n][3],
                'role':row[n][4],
                'password':row[n][5],
                'email':row[n][6],
            })
        data = {
            'users':users,
        }         
    return render(request, 'web_app/userprofile.html',data)

def billinginfo(request):
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM billings WHERE uid='1'""")      
    print(cursor.rowcount) 
    row = cursor.fetchall()
    billings=[]
    data ={
        'billings':None
    }
    a = cursor.rowcount
    if a!=0:
        for n in range(a):
            billings.append({
                'uid':row[n][0],
                'billing_day':row[n][1],
                'amount':row[n][2],
                'bill_id':row[n][3],
                
            })
        data = {
            'billings':billings,
        }         
    return render(request, 'web_app/billinginfo.html',data)

def pastprescriptions(request):
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM prescriptions WHERE uid='1'""")      
    print(cursor.rowcount) 
    row = cursor.fetchall()
    prescriptions=[]
    data ={
        'prescriptions':None
    }
    a = cursor.rowcount
    if a!=0:
        for n in range(a):
            prescriptions.append({
                'prescription':row[n][0],
                'docname':row[n][1],
                'uid':row[n][2],
                'Day':row[n][3],
                'prescription_id':row[n][4],
            })
        data = {
            'prescriptions':prescriptions,
        }         
    return render(request, 'web_app/pastprescriptions.html',data)

def bpapp(request):
    if request.method=='GET':
        user_id = request.GET["uid"]
        testname = request.GET["testname"]
        appdate = request.GET["date"]
        apptime = request.GET["time"]
        cursor = connection.cursor()
        try:
             cursor.execute("""SELECT * FROM users WHERE userid=%s """,[user_id])       
             row = cursor.fetchall()
             a = cursor.rowcount
             if a!=0:
               cursor.execute("""SELECT * FROM testappointments WHERE testname='blood pressure' AND appointment_date=%s """,[appdate])       
               row = cursor.fetchall()
               b = cursor.rowcount
               if b<10:
                cursor.execute("""INSERT INTO testappointments VALUES (%s,%s,%s,%s)""",(user_id,testname,appdate,apptime))      
                return render(request, 'web_app/successful.html')
               else:
                   return render(request, 'web_app/notsuccessful.html')
             else:
                 messages.success(request,'Enter correct values!!')
                 return render(request, 'web_app/bpapp.html')    
        finally:
            cursor.close()  
    return render(request, 'web_app/bpapp.html')

def diabetesapp(request):
    if request.method=='GET':
        user_id = request.GET["uid"]
        testname = request.GET["testname"]
        appdate = request.GET["date"]
        apptime = request.GET["time"]
        
        cursor = connection.cursor()
        try:
             cursor.execute("""SELECT * FROM users WHERE userid=%s """,[user_id])       
             row = cursor.fetchall()
             a = cursor.rowcount
             if a!=0:
               cursor.execute("""SELECT * FROM testappointments WHERE testname='diabetes' AND appointment_date=%s """,[appdate])       
               row = cursor.fetchall()
               b = cursor.rowcount
               if b<10:
                cursor.execute("""INSERT INTO testappointments VALUES (%s,%s,%s,%s)""",(user_id,testname,appdate,apptime)) 
                  
                return render(request, 'web_app/successful.html')
               else: 
                    return render(request, 'web_app/notsuccessful.html')
             else:
                 messages.success(request,'Enter correct values!!')
                 return render(request, 'web_app/diabetesapp.html')    
        finally:
            cursor.close()  
    return render(request, 'web_app/diabetesapp.html')

def reqfill(request):
    
    if request.method=='GET':
        
        user_id = request.GET.get('userid',None)
        requestc = request.GET.get('requestc',None)
        cursor = connection.cursor()
        try:
             cursor.execute("""SELECT * FROM users WHERE userid=%s """,[user_id])       
             row = cursor.fetchall()
             a = cursor.rowcount
             if a!=0:
            
               cursor.execute("""INSERT INTO requests VALUES (%s,%s)""",(user_id,requestc))      
               return render(request, 'web_app/request_c.html')
             else:
                 messages.success(request,'Enter correct values!!')
                 return render(request, 'web_app/request_c.html')    
        finally:
            cursor.close()  
    
    return render(request, 'web_app/request_c.html')




    
    

