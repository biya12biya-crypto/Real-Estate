from django.http import HttpResponse
from django.shortcuts import render

from app_core.models import Property,Category, PropertyImage
from app_buyer.models import Enquiry, Favorite
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
# Create your views here.
@never_cache
@login_required(login_url='/login/')
def viewproperty(request,id):
    c=Property.objects.filter(type=id,approval_status="accepted", registrar_status="approved")
    return render(request, 'viewproperty.html',{"propertyregview":c})

@never_cache
@login_required(login_url='/login/')
def viewcategory(request):
    c=Category.objects.all()
    return render(request, 'viewcategory.html',{"category":c})

@never_cache
@login_required(login_url='/login/')
def aboutview(request,id):
    if request.method=="POST":
        if 'favorite' in request.POST:
            if Favorite.objects.filter(property=id,user=request.user).exists():
                return HttpResponse("<script>alert('Already Exists');window.location='/buyer/favorite/';</script>")
            fav=Favorite()
            fav.user=request.user
            fav.property=Property.objects.get(id=id)
            fav.save()
            return HttpResponse("<script>alert('Item Added to Favorite Successfully');window.location='/buyer/favorite/';</script>")

        else:
            if Enquiry.objects.filter(property=id,user=request.user).exists():
                return HttpResponse("<script>alert('Already Enquired');window.location='/buyer/enquiry/';</script>")
            enq=Enquiry()
            enq.user=request.user
            enq.property=Property.objects.get(id=id)
            enq.save()
            return HttpResponse("<script>alert('Enquiry send successfully');window.location='/buyer/enquiry/';</script>")

    c=Property.objects.get(id=id)
    image=PropertyImage.objects.filter(property=id)

    return render(request, 'aboutview.html',{"category":c,"images":image})

@never_cache
@login_required(login_url='/login/')
def favorite(request):
    f=Favorite.objects.filter(user=request.user)
    return render(request, 'favorite.html',{"aboutview":f})


@never_cache
@login_required(login_url='/login/')
def deletefav(request,id):
    d=Favorite.objects.get(id=id)
    d.delete()
    return HttpResponse("<script>alert('Removed Successfully');window.location='/buyer/favorite/';</script>")

@never_cache
@login_required(login_url='/login/')
def enquiry(request):
    e=Enquiry.objects.filter(user=request.user)
    return render(request, 'enquiry.html',{"aboutview":e})

@never_cache
@login_required(login_url='/login/')
def deleteenq(request,id):
        q=Enquiry.objects.get(id=id)
        q.status='cancelled'
        q.save()
        return HttpResponse("<script>alert('Cancelled Successfully');window.location='/buyer/enquiry/';</script>")

@never_cache
@login_required(login_url='/login/')
def modalview(request):
    e=Enquiry.objects.filter(user=request.user)
    return render(request, 'modalview.html', {"enquiry":e})

@never_cache
@login_required(login_url='/login/')
def deletemodal(request,id):
    d=Enquiry.objects.get(id=id)
    d.delete()
    return HttpResponse("<script>alert('Removed Successfully');window.location='/buyer/modalview/';</script>")

def listings(request):
    propertyregview = Property.objects.filter(approval_status="accepted")
    return render(request, 'listings.html', { 'propertyregview': propertyregview })

