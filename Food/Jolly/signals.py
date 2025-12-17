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

   #if created:
        # instance is the User object that was just saved
        send_welcome_email(instance)

# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
