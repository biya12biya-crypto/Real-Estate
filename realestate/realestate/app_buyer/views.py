from django.http import HttpResponse
from django.shortcuts import render

from app_core.models import Property,Category, PropertyImage
from app_buyer.models import Enquiry, Favorite
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

import joblib
import pandas as pd
from django.shortcuts import render
import os
from django.conf import settings
# Load trained pipeline
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "house_price_xgb_model.pkl")
model = joblib.load(model_path, "rb")



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



# def priceprediction(request):
#     predicted_price = None

#     if request.method == "POST":
#         # Basic fields
#         property_type = request.POST.get("property_type")
#         size_sqft = int(request.POST.get("size_sqft", 0))
#         bhk = int(request.POST.get("bhk", 0))
#         floor_no = request.POST.get("floor_no")
#         total_floors = request.POST.get("total_floors")
#         property_age = int(request.POST.get("property_age", 0))

#         furnished = request.POST.get("furnished")
#         owner_type = request.POST.get("owner_type")
#         facing = request.POST.get("facing")
#         availability = request.POST.get("availability")

#         public_transport = request.POST.get("public_transport")
#         parking = request.POST.get("parking")
#         security = request.POST.get("security")

#         state = request.POST.get("state")
#         city = request.POST.get("city")
#         no_of_sh= int(request.POST.get("no_of_sh", 0))


#         # Checkbox fields (True / False)
#         garden = True if request.POST.get("garden") else False
#         playground = True if request.POST.get("playground") else False
#         clubhouse = True if request.POST.get("clubhouse") else False
#         gym = True if request.POST.get("gym") else False
#         pool = True if request.POST.get("pool") else False
#     return render(request, "priceprediction.html", {"predicted_price": predicted_price})





def predict_price(request):
    prediction = None


    if request.method == "POST":
        try:
            rera = int(request.POST.get("RERA", 0))  # Boolean (0/1)
            bhk_no = int(request.POST.get("BHK_NO"))
            square_ft = float(request.POST.get("SQUARE_FT"))
            ready_to_move = int(request.POST.get("READY_TO_MOVE", 0))
            resale = int(request.POST.get("RESALE", 0))


            input_data = pd.DataFrame([[
                rera,
                bhk_no,
                square_ft,
                ready_to_move,
                resale
            ]], columns=[
                'RERA',
                'BHK_NO.',
                'SQUARE_FT',
                'READY_TO_MOVE',
                'RESALE'
            ])

            raw_prediction = model.predict(input_data)[0]
            prediction = f"₹ {raw_prediction:,.2f} Lakhs"


        except Exception as e:
            prediction = f"Error: {str(e)}"


    return render(request, "predict_house.html", {"prediction": prediction})
