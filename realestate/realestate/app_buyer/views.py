from django.http import HttpResponse
from django.shortcuts import render

from app_core.models import Property,Category, PropertyImage
from app_buyer.models import Enquiry, Favorite

# Create your views here.
def viewproperty(request,id):
    c=Property.objects.filter(type=id)
    return render(request, 'viewproperty.html',{"propertyregview":c})
def viewcategory(request):
    c=Category.objects.all()
    return render(request, 'viewcategory.html',{"category":c})

def aboutview(request,id):
    if request.method=="POST":
        if 'favorite' in request.POST:
            if Favorite.objects.filter(property=id).exists():
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

def favorite(request):
    f=Favorite.objects.filter(user=request.user)
    return render(request, 'favorite.html',{"aboutview":f})



def deletefav(request,id):
    d=Favorite.objects.get(id=id)
    d.delete()
    return HttpResponse("<script>alert('Removed Successfully');window.location='/buyer/favorite/';</script>")


def enquiry(request):
    e=Enquiry.objects.filter(user=request.user)
    return render(request, 'enquiry.html',{"aboutview":e})


def deleteenq(request,id):
        q=Enquiry.objects.get(id=id)
        q.status='cancelled'
        q.save()
        return HttpResponse("<script>alert('Cancelled Successfully');window.location='/buyer/enquiry/';</script>")

def modalview(request):
    e=Enquiry.objects.filter(user=request.user)
    return render(request, 'modalview.html', {"enquiry":e})

def deletemodal(request,id):
    d=Enquiry.objects.get(id=id)
    d.delete()
    return HttpResponse("<script>alert('Removed Successfully');window.location='/buyer/modalview/';</script>")
