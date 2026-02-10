from django.http import HttpResponse
from django.shortcuts import render

from app_core.models import Category, Property, PropertyImage
from app_buyer.models import Enquiry
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
# Create your views here.
@never_cache
@login_required(login_url='/login/')
def propertyreg(request):
    if request.method=='POST':
        name=request.POST.get('name')
        location_url=request.POST.get('location_url')
        type=request.POST.get('type')
        status=request.POST.get('status')
        price=request.POST.get('price')   
        description=request.POST.get('description')
        if Property.objects.filter(name=name,location_url=location_url).exists():
            return HttpResponse("<script>alert('This Property already Exists');window.location='/seller/propertyreg/';</script>") 
        p=Property(name=name,location_url=location_url,type=Category.objects.get(id=type),status=status,price=price,description=description,user=request.user)
        p.type=Category.objects.get(id = type)
        p.save()
        images = request.FILES.getlist('img')
        for img in images:
            PropertyImage.objects.create(
                property=p,
                img=img
            )

        return HttpResponse("<script>alert('Property added successfully');window.location='/sellerdashboard/';</script>") 
    cat =Category.objects.all()
    return render(request, "propertyreg.html", {"list": cat})

    return render(request, 'propertyreg.html')
    
@never_cache
@login_required(login_url='/login/')
def propertyregview(request):
     pr =Property.objects.all()
     return render(request, "propertyregview.html", {"propertyregview": pr})

@never_cache
@login_required(login_url='/login/')
def enquiryview(request):
    if request.method=="POST":
        id=request.POST.get("id")
        msg=request.POST.get("msg")

        c =Enquiry.objects.get(id =id)
        c.status="approved"
        c.msg=msg
        c.save()
    n= Enquiry.objects.filter(status="requested",property__user=request.user)
    return render(request, "enquiryview.html", {"enquiry": n})

@never_cache
@login_required(login_url='/login/')
def deleteenqv(request,id):
    r=Enquiry.objects.get(id=id)
    r.delete()
    return HttpResponse("<script>alert('Removed Successfully');window.location='/seller/enquiryview/';</script>")

@never_cache
@login_required(login_url='/login/')
def enqaccept(request):
    
        return HttpResponse("<script>alert('Enquiry Approved Successfully');window.location='/seller/enquiryview/';</script>")
    