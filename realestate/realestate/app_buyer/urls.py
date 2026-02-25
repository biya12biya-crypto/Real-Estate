from django.urls import path
from app_buyer import views

app_name="buyer"
urlpatterns = [
    path("viewproperty/<int:id>",views.viewproperty,name="viewproperty"),
    path("viewcategory/",views.viewcategory,name='viewcategory'),
    path("aboutview/<int:id>",views.aboutview,name='aboutview'),    
    path("favorite/",views.favorite,name='favorite'),     
     path("deletefav/<int:id>",views.deletefav,name='deletefav'), 
     path("enquiry/",views.enquiry,name='enquiry'),
     path("deleteenq/<int:id>",views.deleteenq,name='deleteenq'),
   path("modalview/",views.modalview,name='modalview'),
    path("deletemodal/<int:id>",views.deletemodal,name='deletemodal'),
 path("listings/",views.listings,name='listings'),
 path("predict_house/",views.predict_house,name='predict_house'),



]