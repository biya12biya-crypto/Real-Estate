
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
        price=models.CharField()
        description=models.CharField()
        role_choices=[('requested','requested'),('accepted','acceped'),('rejected','rejected')]
        approval_status=models.CharField(("Approval_Status"),choices=role_choices,null=False,blank=False,default='requested')
        user=models.ForeignKey(User,on_delete=models.CASCADE,default=1,related_name="property_seller")


class PropertyImage(models.Model):
        img=models.ImageField(upload_to="media/",null=True,blank=True) 
        property=models.ForeignKey(Property,on_delete=models.CASCADE,related_name="images")


        



