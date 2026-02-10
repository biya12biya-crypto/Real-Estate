from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models


class User(AbstractUser):
    """
    Default custom user model for RealEstate.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True,null=True, max_length=255)
    username=CharField(_("Username"),unique=True)
    password=CharField(_("Password"),unique=True)
    email=models.EmailField(_("email"),unique=True)
    role_choices=[('buyer','buyer'),('seller','seller'), ('both', 'both'), ('admin', 'admin')]
    role=models.CharField(_("Role"),choices=role_choices,null=False,blank=False,default='admin')

    



    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
