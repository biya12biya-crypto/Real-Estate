from django.db import models

# Create your models here.

from realestate.users.models import User

class Otp(models.Model):
    otp=models.CharField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="otp_user")
    otp_date=models.DateField(auto_now_add=True)
