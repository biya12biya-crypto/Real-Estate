from django.http import HttpResponse
from django.shortcuts import render

from app_core.models import Buyer, Category, District, Location, Property, Seller
from realestate.users.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail

# Create your views here.
@never_cache
@login_required(login_url='/login/')
def dist(request):
    if request.method=='POST':
        name=request.POST.get('distname')
        print("success ")
        if District.objects.filter(name = name ).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/core/dist/';</script>")
        dist=District()
        dist.name=name
        dist.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='/core/dist/';</script>")
    else:
        return render(request,"district.html")

@never_cache
@login_required(login_url='/login/')
def location(request):
    if request.method=='POST':
        name=request.POST.get('locationname')
        dis=request.POST.get('name1')
        print("success ")
        if Location.objects.filter(name = name,dis=dis ).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/core/location/';</script>")
        loc=Location()
        loc.name=name
        loc.dis=District.objects.get(id = dis)
        loc.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='/core/location/';</script>")
    else:
        v=District.objects.all()
        return render(request,"location.html",{"list":v})
    
@never_cache
@login_required(login_url='/login/')   
def distview(request):
     dt = District.objects.all()
     return render(request,"viewdist.html",{"distview":dt})    

@never_cache
@login_required(login_url='/login/')
def distde(request,name):
     d=District.objects.get(id=name)
     d.delete()
     return HttpResponse("<script>alert('Deleted Successfully');window.location='/core/distview/';</script>")

@never_cache
@login_required(login_url='/login/')
def districtup(request,name):
    d=District.objects.get(id=name)
    if request.method=="POST":
        name=request.POST.get('name')
        if District.objects.filter(name=name).exists():
            return HttpResponse("<script>alert('District already exists');window.location='/core/distview';</script>")
        d.name=name
        d.save()
        return HttpResponse("<script>alert('District added successfully');window.location='/core/distview';</script>")
    return render(request,'districtup.html',{"distview":d}) 

@never_cache
@login_required(login_url='/login/')
def  locationview(request):
    lc = Location.objects.all()
    return render(request,"locationview.html",{"locationview":lc})

@never_cache
@login_required(login_url='/login/')
def deleteloc(request,id):
    d=Location.objects.get(id=id)
    d.delete()
    return HttpResponse("<script>alert('Deleted Successfully');window.location='/core/locationview/';</script>")

@never_cache
@login_required(login_url='/login/')
def locationup(request,id):
    up = Location.objects.get(id=id)
    if request.method=="POST":
        name = request.POST.get('name')
        dis = request.POST.get('dis')
        # return HttpResponse(dis)
        if Location.objects.filter( name=name, dis=dis ).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='';</script>")
        up.name = name
        up.dis = District.objects.get(id = dis)
        up.save()
        return HttpResponse("<script>alert('Updated Successfully');window.location='/core/locationview/';</script>")
    list=District.objects.all()
    return render(request,"locationup.html",{"locationv":up,"list":list})

@never_cache
@login_required(login_url='/login/')
def category(request):
    if request.method=='POST':
        name=request.POST.get('name')
        description=request.POST.get('description')
        print("success ")
        if Category.objects.filter(name = name ).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/core/category/';</script>")
        cat=Category()
        cat.name=name
        cat.description=description
        if len(request.FILES) !=0:
            img = request.FILES['img']
        else:
            img = 'Images/default.jpg'
        cat.img=img
        cat.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='/core/category/';</script>")
    else:
        return render(request,"category.html")

@never_cache
@login_required(login_url='/login/')    
def viewcat(request):
    cv=Category.objects.all()
    return render(request,"viewcat.html",{"list":cv})   

@never_cache
@login_required(login_url='/login/')
def catedl(request,name):
    d =Category.objects.get(id =name)
    d.delete()
    return HttpResponse("<script>alert('Delete Successfully');window.location='/core/viewcat/';</script>")

@never_cache
@login_required(login_url='/login/')
def cateup(request,name):
    up = Category.objects.get(id=name)
    if request.method=="POST":
        cname = request.POST.get('name')
        desc = request.POST.get('description')
        img = request.FILES.get('img')

        if Category.objects.filter(name=cname).exclude(id=name).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/core/category/';</script>")
        up.name=cname
        up.description=desc
        if img:
            up.img=img
        up.save()
        return HttpResponse("<script>alert('Updated Successfully');window.location='/core/viewcat/';</script>")
    return render(request,"categoryedit.html",{"catv":up})


@never_cache
@login_required(login_url='/login/')
def sellerregview(request):
     sellers =Seller.objects.all()
     return render(request, "sellerregview.html", {"sellerregview": sellers})

@never_cache
@login_required(login_url='/login/')
def buyerregview(request):
     buyers =Buyer.objects.all()
     return render(request, "buyerregview.html", {"buyerregview": buyers})

@never_cache
@login_required(login_url='/login/')
def adminviewproperty(request):
       adminv =Property.objects.all()
       return render(request, "adminviewproperty.html", {"adminviewproperty": adminv})
       

   

@never_cache
@login_required(login_url='/login/')
def proreject(request,name):
    r =Property.objects.get(id =name)
    r.approval_status="rejected"
    return HttpResponse("<script>alert('Rejected Successfully');window.location='/core/adminviewproperty/';</script>")

@never_cache
@login_required(login_url='/login/')
def proaccept(request,name):
    a =Property.objects.get(id =name)
    a.approval_status="accepted"
    a.save()
    return HttpResponse("<script>alert('Property Accepted Successfully');window.location='/core/adminviewproperty/';</script>")

def registrarreg(request):
    if request.method == 'POST':
        role_select = "registrar"
        name = request.POST.get('registrar_name')
        email = request.POST.get('email')
        
        user = User()
        user.username = "user123"
        user.email = email
        user.name = name
        user.role = role_select
        user.set_password("pass123") 
        user.save()
        send_mail(subject="Registration successfull", message=f"Hai {name} Welcome To KeralaNest", from_email=None, recipient_list=[email])
        return HttpResponse("<script>alert('Registration Successfull.');window.location='/core/registrarreg/';</script>")
    registrarreg=User.objects.filter(role="registrar")
    return render(request,"registrarreg.html",{"registrarreg":registrarreg})

def registrarlogin(request):
    return render(request,"login.html")
def registratlogin(request):
    if request.method == 'POST':
        username = request.POST.get('user123')
        password = request.POST.get('pass123')
        user = User.objects.filter(role="registrar").first()
        if user:
            if user.check_password(password):
                login(request, user)
                return redirect('registrarhome')
            else:
                return HttpResponse("<script>alert('Invalid password');window.location='/core/registrarlogin/';</script>")
        else:
            return HttpResponse("<script>alert('Invalid email');window.location='/core/registrarlogin/';</script>")

def regaccept(request, id):
    prop = Property.objects.get(id=id)

    # get a registrar (basic version)
    registrar = User.objects.get(role="registrar")

    # assign registrar
    prop.registrar = registrar

    # update registrar status
    prop.registrar_status = "assigned"

    prop.save(update_fields=["registrar", "registrar_status"])

    return HttpResponse(
        "<script>"
        "alert('Property assigned successfully');"
        "window.location='/core/adminviewproperty/';"
        "</script>"
    )

@never_cache
@login_required(login_url='/login/')
def adminviewpayment(request):
       payment =Property.objects.all()
       return render(request, "adminviewpayment.html", {"adminviewpayment": payment})


def bestseller(request):
    seller_data = (
        Property.objects
        .values('seller__seller_name')
        .annotate(property_count=Count('id'))
        .order_by('-property_count')
    )

    labels = [
        item['seller__seller_name']
        for item in seller_data
        if item['seller__seller_name']
    ]

    data = [
        item['property_count']
        for item in seller_data
        if item['seller__seller_name']
    ]

    context = {
        'labels': labels,
        'data': data,
    }

    return render(request, "bestseller.html", context)