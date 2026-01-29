from pyexpat.errors import messages
from weakref import ref
from django.http import HttpResponse
from django.shortcuts import redirect, render

from app_core.models import Buyer, Property, Seller
from realestate.users.models import User
from django.contrib.auth import authenticate,login





def admin(request):
    return render(request, 'admindashboard.html')
def guest(request):
    return render(request, 'guestdashboard.html')


def log (request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            if user.role=="admin":
                login(request,user)
                return HttpResponse("<script>alert('Login Successfully');window.location='/admin/';</script>")
            elif user.role=="seller":
                login(request,user)
                return HttpResponse("<script>alert('Login Successfully');window.location='/sellerdashboard/';</script>")
            elif user.role=="buyer":
                login(request,user)
                return HttpResponse("<script>alert('Login Successfully');window.location='/buyerdashboard/';</script>")
            else:
                return HttpResponse("<script>alert('Invalid Username or Password');window.location='/login/';</script>")

        else:
           return HttpResponse("<script>alert('Invalid Username or Password');window.location='/login/';</script>")
    else:
        return render(request,"login.html")
    
def sellerreg(request):
    if request.method=='POST':
        username=request.POST.get('username')
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')   
        contact=request.POST.get('contact')
        address=request.POST.get('address')
        
        if not username or not password:
            # reg(request,user)
            return HttpResponse("<script>alert('Username and Password are required');window.location='/sellerreg/';</script>") 
        if User.objects.filter(username=username).exists():
            # reg(request,user)
            return HttpResponse("<script>alert('Username already Exists');window.location='/sellerreg/';</script>") 
        user=User()
        user.username=username
        user.email=email
        user.name=name
        user.role="seller"
        user.set_password(password)
        user.save()
        Seller.objects.create(user=user,contact=contact,address=address)
        # messages.success(request,"Registration Successfull.Please Login")
        # return redirect('app_dashboard:login')
        return HttpResponse("<script>alert('Registration Successfull.Please Login');window.location='/login/';</script>") 
    return render(request,'sellerreg.html')


def buyerreg(request):
    if request.method=='POST':
        username=request.POST.get('username')
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')   
        contact=request.POST.get('contact')
        address=request.POST.get('address')
        
        if not username or not password:
            # reg(request,user)
            return HttpResponse("<script>alert('Username and Password are required');window.location='/buyerreg/';</script>") 
        if User.objects.filter(username=username).exists():
            # reg(request,user)
            return HttpResponse("<script>alert('Username already Exists');window.location='/buyerreg/';</script>") 
        user=User()
        user.username=username
        user.email=email
        user.name=name
        user.role="buyer"
        user.set_password(password)
        user.save()
        Buyer.objects.create(user=user,contact=contact,address=address)
        # messages.success(request,"Registration Successfull.Please Login")
        # return redirect('app_dashboard:login')
        return HttpResponse("<script>alert('Registration Successfull.Please Login');window.location='/login/';</script>") 
    return render(request,'buyerreg.html')

def sellerdashboard(request):
    return render(request, 'sellerdashboard.html')

def buyerdashboard(request):
    return render(request, 'buyerdashboard.html')



