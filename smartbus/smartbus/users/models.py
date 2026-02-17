from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models 

class User(AbstractUser):
    """
    Default custom user model for smartbus.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, null=True, max_length=255)
    username = CharField(_("Username"),unique=True)
    password = CharField(_("User Password"),unique=True)
    email = models.EmailField(_("User Email"),unique=True)
    rolechoice = [('Bus operator','Bus operator'),('Passengers','Passengers')]
    role = models.CharField(choices=rolechoice, blank=False, default="Admin", null=False)
    
    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
    
