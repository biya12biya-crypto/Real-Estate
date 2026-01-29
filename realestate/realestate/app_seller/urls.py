from django.urls import path

from app_seller import views


app_name="seller"
urlpatterns = [
     path("propertyreg/",views.propertyreg,name='propertyreg'),
     path("propertyregview/",views.propertyregview),
     path("enquiryview/",views.enquiryview,name='enquiryview'),
     path("deleteenqv/<int:id>/",views.deleteenqv,name='deleteenqv'),
     path("enqaccept",views.enqaccept,name='enqaccept'),
]