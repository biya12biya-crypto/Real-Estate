from django.urls import path

from app_seller import views


app_name="seller"
urlpatterns = [
     path("propertyreg/",views.propertyreg,name='propertyreg'),
     path("propertyregview/",views.propertyregview),
     path("enquiryview/",views.enquiryview,name='enquiryview'),
     path("deleteenqv/<int:id>/",views.deleteenqv,name='deleteenqv'),
     path("enqaccept",views.enqaccept,name='enqaccept'),
     path("payment1",views.payment1,name='payment1'),
     path("payment2/<int:plan>/",views.payment2,name='payment2'),
     path("propertyedit/<int:id>/",views.propertyedit,name='propertyedit'),
     path("propertydl/<int:id>/",views.propertydl,name='propertydl'),
]