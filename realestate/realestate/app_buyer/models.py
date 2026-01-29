from django.db import models

from app_core.models import Property
from realestate.users.models import User

# Create your models here.
class Favorite(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="buyer_favorite")
    property=models.ForeignKey(Property,on_delete=models.CASCADE,related_name="property_favorite")
    created_at=models.DateField(auto_now_add=True)

class Enquiry(models.Model):   
    msg=models.CharField()
    status_choices=[('requested','requested'),('approved','approved'),('rejected','rejected'),('cancelled','cancelled')]
    status=models.CharField(choices=status_choices,default="requested")
    enq_date=models.DateField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="buyer_enquiry")
    property=models.ForeignKey(Property,on_delete=models.CASCADE,related_name="property_enquiry")