from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.core.validators import RegexValidator

class AppUserManager(UserManager):

    def is_trusty_comment(self):
        # Implement logic if needed
        pass

    def get_admin(self):
        """Returns the first superuser (admin)."""
        return self.filter(is_superuser=True).first()

class AppUser(AbstractUser):
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+254712345678'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=15, unique=True, blank=True, null=True)

    objects = AppUserManager()
