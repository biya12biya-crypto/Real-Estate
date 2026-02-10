from django.utils import timezone
from pyexpat.errors import messages
from weakref import ref
from django.http import HttpResponse
from django.shortcuts import redirect, render

from app_core.models import Buyer, Property, Seller
from realestate.users.models import User
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail
from app_dashboard.models import Otp
import random
from django.contrib.auth.hashers import make_password


@never_cache
@login_required(login_url='/login/')
def admin(request):
    return render(request, 'admindashboard.html')

@never_cache
@login_required(login_url='/login/')
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
        send_mail(subject="Registration successfull",message=f"Hai {name} Welcome To KeralaNest",from_email=None,recipient_list=[email])

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
        send_mail(subject="Registration successfull",message=f"Hai {name}",from_email=None,recipient_list=[email])
        Buyer.objects.create(user=user,contact=contact,address=address)
        # messages.success(request,"Registration Successfull.Please Login")
        # return redirect('app_dashboard:login')
        return HttpResponse("<script>alert('Registration Successfull.Please Login');window.location='/login/';</script>") 
    return render(request,'buyerreg.html')

@never_cache
@login_required(login_url='/login/')
def sellerdashboard(request):
    return render(request, 'sellerdashboard.html')

@never_cache
@login_required(login_url='/login/')
def buyerdashboard(request):
    return render(request, 'buyerdashboard.html')



def logout_view(request):
    logout(request)
    return HttpResponse(
        "<script>alert('Logged out successfully');window.location='/login/';</script>"
    )





def forget(request):
    msg = ""

    if request.method == "POST":
        email = request.POST.get("email")

        if not User.objects.filter(email=email).exists():
            msg = "Email not registered."
            return render(request, "forget.html", {"msg": msg})

        user_data = User.objects.get(email=email)
        request.session["id"] = user_data.id

        random_otp = random.randint(100000, 999999)

        # UPDATE if exists, CREATE if not
        Otp.objects.update_or_create(
            user=user_data,
            defaults={
                "otp": random_otp,
                "otp_date": timezone.now()
            }
        )

        send_mail(
            subject="One Time Password",
            message=f"Hai {user_data.username}\nYour OTP for resetting password is {random_otp}.",
            from_email=None,
            recipient_list=[email]
        )

        return redirect("dashboard:verify_otp")

    return render(request, "forget.html", {"msg": msg})



def verify_otp(request):
    msg = ""

    if request.method == "POST":
        action = request.POST.get("action")
        user_id = request.session.get("id")

        if not user_id:
            msg = "Session expired. Please try again."
            return render(request, "verify_otp.html", {"msg": msg})

        user_data = User.objects.get(id=user_id)

        # ✅ VERIFY OTP
        if action == "verify":
            entered_otp = request.POST.get("otp")

            try:
                otp_data = Otp.objects.get(user=user_data)
            except Otp.DoesNotExist:
                msg = "OTP not found. Please resend OTP."
                return render(request, "verify_otp.html", {"msg": msg})

            if str(otp_data.otp) == entered_otp:
                return redirect("dashboard:reset")
            else:
                msg = "Invalid OTP"

        # 🔁 RESEND OTP
        elif action == "resend":
            random_otp = random.randint(100000, 999999)

            Otp.objects.update_or_create(
                user=user_data,
                defaults={
                    "otp": random_otp,
                    "otp_date": timezone.now()
                }
            )

            send_mail(
                subject="One Time Password",
                message=f"Hai {user_data.username}\nYour OTP for resetting password is {random_otp}.",
                from_email=None,
                recipient_list=[user_data.email]
            )

            msg = "OTP resent successfully"

    return render(request, "verify_otp.html", {"msg": msg})


def reset(request):
    msg = ""
    id = request.session.get("id")

    if request.method == "POST":
        pwd = request.POST.get("password")
        cpwd = request.POST.get("confirm")

        if pwd == cpwd:
            user = User.objects.get(id=id)
            user.password = make_password(pwd)
            user.save()
            msg = "Password reset successful"
            return HttpResponse("<script>alert('Password Successfully Resetted.Please Login');window.location='/login/';</script>") 
        else:
            msg = "Passwords do not match"
            return HttpResponse("<script>alert('Password do not match');window.location='/login/';</script>") 
    return render(request, "reset.html", {"msg": msg})

   

  

