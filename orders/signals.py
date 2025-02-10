from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order
from .utils import send_sms, send_admin_email


@receiver(post_save, sender=Order)
def notify_on_order_creation(sender, instance, created, **kwargs):
    if created:  # Only notify when a new order is placed
        user = instance.user  # The user who placed the order
        if not user:
            return  # Skip if user is missing

        sms_message = f"Dear {user.first_name}, your order #{instance.id} has been placed successfully. We will notify you once it is processed."

        # Send SMS (if user has a phone number)
        if hasattr(user, 'phone') and user.phone:
            send_sms(user.phone, sms_message)

        # Send Email to Admin
        send_admin_email(instance)
