from django.db import models

from shared.models import TimestampedModel
from users.models import AppUser


# Create your models here.
class Customer(TimestampedModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(  # Use OneToOneField to associate exactly one User to one Customer
        AppUser,  # Referring to the AppUser model for the user
        related_name='customer',
        null=True, blank=True,
        on_delete=models.SET_NULL,  # If the user is deleted, the customer becomes null
        verbose_name='User'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name_plural = "Customers"