from email import message
from multiprocessing import context
from django.shortcuts import render,HttpResponse
from .models import Role,Employee
from datetime import datetime
from django.db.models import Q
from django.contrib import messages
# Create your views here.


def index(request):
    return render(request,'index.html')

def all_emp(request):
    emps=Employee.objects.all()
    context={
        'emps':emps,
    }
    #print(context)
    return render(request,'view_all_emp.html',context)

def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = request.POST['salary']
        bonus = request.POST['bonus']
        phone= request.POST['phone']
        dept = request.POST['dept']
        role = request.POST['role']
        
        new_emp=Employee(first_name=first_name,last_name=last_name,salary=salary,bonus=bonus,phone_number=phone,dept_id=dept,role_id=role,hire_date=datetime.now())
        new_emp.save()
        messages.success(request,'Employee added Successfully')
        return render(request,'add_emp.html')
    elif request.method=='GET':
     return render(request,'add_emp.html')
    else:
        return HttpResponse("An error Occured! Employee Has Not Been added")
    
def remove_emp(request, emp_id=0):
   
    emps=Employee.objects.all()
    context={
        'emps':emps
    }
    if emp_id:
        try:
            emp_to_be_removed= Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            messages.success(request,'Employee Removed Succssesfully')
            return render(request,'remove_emp.html',context)
        except:
            return render(request,'remove_emp.html',context)
   
    #print(context)
    return render(request,'remove_emp.html',context)
   
   
    
def filter_emp(request):
    if request.method=='POST':
        name=request.POST['name']
        dept=request.POST['dept']
        role=request.POST['role']
        emps=Employee.objects.all()
        if name:
            emps=emps.filter(Q(first_name__icontains=name) | Q (last_name__icontains=name))
        if dept:
            emps=emps.filter(dept__name__icontains=dept)
        if role:
            emps=emps.filter(role__name__icontains=role) 
        
        context={
            'emps':emps,
        }       
        return render(request,'view_all_emp.html',context)

    elif request.method=='GET':
        return render(request,'filter_emp.html')
    else:
        return HttpResponse("An Exception Occurred")
        