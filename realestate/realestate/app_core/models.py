
from django.db import models

from realestate.users.models import User


class District(models.Model):
        name=models.CharField(max_length=20)
       
class Location(models.Model):        
           name=models.CharField(max_length=20)
           dis=models.ForeignKey(District,on_delete=models.CASCADE,default=1)

class Category(models.Model):
    name=models.CharField(max_length=20)
    description=models.CharField()
    img=models.ImageField(upload_to="media/",null=True,blank=True) 

class Seller(models.Model):
        contact=models.CharField()
        address=models.CharField()
        location=models.CharField()
        user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)

class Buyer(models.Model):
        contact=models.CharField()
        address=models.CharField()
        location=models.CharField()
        user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)

class Property(models.Model):   
        name=models.CharField()
        location_url=models.CharField()
        type=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
        status=models.CharField()
        status_choices=[
            ('pending', 'Pending'),
            ('assigned', 'Assigned'),
            ('approved', 'Approved'),
            ('rejected','rejected')
        ]
        registrar_status=models.CharField(max_length=20, choices=status_choices, default='pending')
        
        price=models.CharField()
        description=models.CharField()
        role_choices=[('requested','requested'),('accepted','acceped'),('rejected','rejected')]
        approval_status=models.CharField(("Approval_Status"),choices=role_choices,null=False,blank=False,default='requested')
        
        user=models.ForeignKey(User,on_delete=models.CASCADE,default=1,related_name="property_seller")
        registrar=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="registrar")
        


class PropertyImage(models.Model):
        img=models.ImageField(upload_to="media/",null=True,blank=True) 
        property=models.ForeignKey(Property,on_delete=models.CASCADE,related_name="images")


class Document(models.Model):
    property = models.ForeignKey( Property, related_name="documents",  on_delete=models.CASCADE)
    doc = models.ImageField(upload_to="documents/", null=True, blank=True)     


class payment(models.Model):
       payment_date=models.DateField(auto_now_add=True)
       expiry_date=models.DateField()
       user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
       duration=models.CharField()
       amount=models.FloatField(null=True,blank=True)

