from django.urls import path
from app_core import views

app_name="core"
urlpatterns = [
  
  path("dist/",views.dist,name='dist'),
  path("location/",views.location,name='location'),
  path("distview/",views.distview,name='distview'),
  path("distde/<int:name>",views.distde,name='distde'),
  path("districtup/<int:name>",views.districtup,name='districtup'),
  path("locationview/",views.locationview,name='locationview'),
  path("deleteloc/<int:id>/",views.deleteloc,name='deleteloc'),
  path("locationup/<int:id>/", views.locationup, name="locationup"),
  path("category/",views.category,name='category'),
  path("viewcat/",views.viewcat,name='viewcat'),
  path("catedl/<int:name>", views.catedl, name="catdl"),
  path("cateup/<int:name>", views.cateup, name="catup"),
 
  path("buyerregview/",views.buyerregview,name='buyerregview'),
  path("adminviewproperty/",views.adminviewproperty,name='adminviewproperty'),
  path("proreject/<int:name>",views.proreject,name='proreject'),
  path("proaccept/<int:name>",views.proaccept,name='proaccept'),
  path("sellerregview/",views.sellerregview,name='sellerregview'),
  
  path("registrarreg/",views.registrarreg,name='registrarreg'),
  path("regaccept/<int:id>",views.regaccept,name='regaccept'),
  path("adminviewpayment/",views.adminviewpayment,name='adminviewpayment'),
   path("bestpro/",views.bestpro,name='bestpro'),
   path('seller_payments/', views.seller_payment_list, name='seller_payment_list'),
path('seller_payment_excel/', views.seller_payment_excel, name='seller_payment_excel'),
    ]