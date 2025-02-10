from django.core.mail import send_mail
from django.conf import settings
import africastalking
from users.models import AppUser  # Ensure this is your admin user model
from orders.models import Order

# Initialize Africa's Talking
africastalking.initialize(settings.AT_USERNAME, settings.AT_API_KEY)
sms = africastalking.SMS


def get_admin_email():
    """
    Fetches the first available admin email.
    Assumes superusers are admins.
    """
    admin_user = AppUser.objects.filter(is_superuser=True).first()
    return admin_user.email if admin_user else settings.ADMIN_EMAIL


def send_sms(phone_number: str, message: str):
    """
    Sends an SMS to the given phone number using Africa's Talking API.
    """
    try:
        response = sms.send(message, [phone_number], sender_id=settings.AT_SENDER_ID)
        print("SMS Response:", response)
        return response
    except Exception as e:
        print("SMS Error:", str(e))
        return None


def send_admin_email(order: Order):
    """
    Sends an email to the admin with order details.
    """
    admin_email = get_admin_email()
    user = order.user  # The user who placed the order

    subject = f"New Order Placed - #{order.id}"
    message = f"""
    A new order has been placed.

    Order ID: {order.id}
    Placed By: {user.first_name} {user.last_name}
    Email: {user.email}
    Phone: {getattr(user, 'phone', 'N/A')}
    Total Items: {order.order_items.count()}
    Order Status: {order.get_order_status_display()}

    Order Items:
    {', '.join([item.name for item in order.order_items.all()])}

    Regards,
    Savannah E-Commerce System
    """

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [admin_email],
        fail_silently=False,
    )
