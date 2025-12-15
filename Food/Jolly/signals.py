# your_app/signals.py

from django.contrib.auth.signals import user_logged_in
from .models import CartItem
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

# Import the email function we just created
from .emails import send_welcome_email

@receiver(post_save, sender=User)
def handle_new_user_signup(sender, instance, created, **kwargs):

    # Triggers the welcome email ONLY when the User object is first created (signed up).

   if created:
        # instance is the User object that was just saved
        send_welcome_email(instance)


#Function for merging non login-user items before login in as user
@receiver(user_logged_in)
def merge_guest_cart_with_user_cart(sender, request, user, **kwargs):
    session_key = request.session.session_key

    if not session_key:
        return  # no guest cart

    # Get guest cart items
    guest_items = CartItem.objects.filter(
        session_key=session_key,
        user__isnull=True
    )

    for item in guest_items:
        # Check if user already has this food item
        user_item = CartItem.objects.filter(
            user=user,
            food_name=item.food_name
        ).first()

        if user_item:
            # Merge quantities
            user_item.quantity += item.quantity
            user_item.save()
            item.delete()  # remove guest item
        else:
            # Assign guest item to user
            item.user = user
            item.session_key = None
            item.save()
