from django.http import HttpResponse
from django.shortcuts import redirect, render

from app_core.models import Category, Property, PropertyImage,payment,Document
from app_buyer.models import Enquiry
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from datetime import date
from django.utils import timezone
from dateutil.relativedelta import relativedelta
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
        documents = request.FILES.getlist('doc')
        for doc in documents:
            Document.objects.create(
                property=p,
                doc=doc
            )
        return HttpResponse("<script>alert('Property added successfully');window.location='/sellerdashboard/';</script>") 
    cat =Category.objects.all()
    pay = payment.objects.filter(user=request.user).order_by('-id').first()

    today = timezone.now().date()

    # ❌ No payment OR plan expired → redirect to payment page
    if not pay or today > pay.expiry_date:
        return redirect('seller:payment1')

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
    

@never_cache
@login_required(login_url='/login/')
def payment1(request):
    return render(request, "payment1.html")
    
 
@never_cache
@login_required(login_url='/login/')
def payment2(request, plan):
    plans = {
        3: {
            "name": "Basic Plan",
            "duration": "3 Months",
            "amount": 999
        },
        6: {
            "name": "Standard Plan",
            "duration": "6 Months",
            "amount": 1799
        },
        12: {
            "name": "Premium Plan",
            "duration": "1 Year",
            "amount": 2999
        }
    }

    selected_plan = plans.get(plan)

    if not selected_plan:
         return redirect('seller:payment1')

    if not plan:
        return redirect('seller:payment1')

     
    # If Confirm & Pay button is clicked
    if request.method == "POST":
        today = date.today()
        if plan==3:
            amount=999
            duration="3 Month"
            exp=today + relativedelta(months=3)
        elif plan==6:
            amount=1799
            duration="6 Month"
            exp=today + relativedelta(months=6)
        elif plan==12:
            amount=2999
            duration="12 Month"
            exp=today + relativedelta(months=12)
        else:
            return HttpResponse("<script>alert('Invalid choice');window.location='/seller/payment1'")
        if payment.objects.filter(user=request.user).exists():
            p=payment.objects.get(user=request.user)
            p.expiry_date=exp
            p.duration=duration
            p.amount=amount
            p.payment_date=today
            p.save()
        pay=payment()
        pay.expiry_date=exp
        pay.duration=duration
        pay.amount=amount
        pay.user=request.user
        pay.save()
        # here you will integrate payment gateway later
        # For now, assume payment is successful
        return redirect('seller:propertyreg')
        
    context = {
        'plan_name': selected_plan['name'],
        'plan_duration': selected_plan['duration'],
        'amount': selected_plan['amount'],
        'plan':plan
    }

    return render(request, 'payment2.html', context)   


# @never_cache
# @login_required(login_url='/login/')
# def propertyedit(request,id):
#     up = Property.objects.get(id=id)
#     if request.method=="POST":
#         name=request.POST.get('name')
#         location_url=request.POST.get('location_url')
#         type=request.POST.get('type')
#         status=request.POST.get('status')
#         price=request.POST.get('price')   
#         description=request.POST.get('description')
#         if Property.objects.filter(name=name,location_url=location_url).exists():
#             return HttpResponse("<script>alert('This Property already Exists');window.location='/seller/propertyreg/';</script>") 
#         p=Property(name=name,location_url=location_url,type=Category.objects.get(id=type),status=status,price=price,description=description,user=request.user)
#         p.type=Category.objects.get(id = type)
#         p.save()
#         images = request.FILES.getlist('img')
#         for img in images:
#             PropertyImage.objects.create(
#                 property=p,
#                 img=img
#             )
#         documents = request.FILES.getlist('doc')
#         for doc in documents:
#             Document.objects.create(
#                 property=p,
#                 doc=doc
#             )
#     return HttpResponse("<script>alert('Property Edited successfully');window.location='/sellerdashboard/';</script>") 

@never_cache
@login_required(login_url='/login/')
def propertyedit(request, id):

    up = Property.objects.get(id=id)
    list = Category.objects.all()

    if request.method == "POST":

        up.name = request.POST.get('name')
        up.location_url = request.POST.get('location_url')
        type_id = request.POST.get('type')
        up.type = Category.objects.get(id=type_id)
        up.status = request.POST.get('status')
        up.price = request.POST.get('price')
        up.description = request.POST.get('description')

        up.save()

        images = request.FILES.getlist('img')
        for img in images:
            PropertyImage.objects.create(
                property=up,
                img=img
            )

        documents = request.FILES.getlist('doc')
        for doc in documents:
            Document.objects.create(
                property=up,
                doc=doc
            )

        return HttpResponse("<script>alert('Property Edited Successfully');window.location='/sellerdashboard/';</script>")

    return render(request, "propertyedit.html", {
        "property": up,
        "list": list
    })



@never_cache
@login_required(login_url='/login/')
def propertydl(request, id):

    d = Property.objects.get(id=id)
    d.delete()

    return HttpResponse("<script>alert('Delete Successfully');window.location='/sellerdashboard/';</script>")