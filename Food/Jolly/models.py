import random

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)
    food_name = models.CharField(max_length=200)
    food_price = models.DecimalField(max_digits=10, decimal_places=2)
    food_image = models.ImageField(upload_to='food_images/')
    quantity = models.IntegerField(default=1 )
    added_at = models.DateTimeField(auto_now_add=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    address_text = models.CharField(max_length=255, null=True, blank=True)

    def get_total_price(self):
        return self.food_price * self.quantity

    def __str__(self):
        return f"{self.food_name} - {self.quantity}"


# models.py
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username


from django.db import models

class SecurityLog(models.Model):
    EVENT_TYPES = (
        ('LOGIN_FAIL', 'Failed Login Attempt'),
        ('SENSITIVE_ACCESS', 'Sensitive Data Access'),
        ('BREAKAGE', 'Backend Error (500)'),
        ('DATA_VOL', 'High Data Usage'),
    )

    timestamp = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(null=True, blank=True)
    path = models.CharField(max_length=255)
    details = models.TextField()
    severity = models.IntegerField(default=1)  # 1=Low, 3=Critical

    def __str__(self):
        return f"{self.event_type} - {self.ip_address} at {self.timestamp}"


#Delivery details for Driver
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, help_text="Driver's contact number")
    vehicle_plate = models.CharField(max_length=20, help_text="e.g., AS-202-26")

    def __str__(self):
        return self.user.username


class Delivery(models.Model):
    driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='deliveries',
        null=True
    )

    customer_name = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    lat = models.FloatField()
    lng = models.FloatField()

    phone_number = models.CharField(max_length=15, null=True, blank=True)
    landmark = models.CharField(max_length=255, null=True, blank=True)
    token = models.CharField(max_length=6, blank=True, null=True)  # The 6-digit code
    items_json = models.TextField(null=True, blank=True)   # Stores list of food items
    status = models.CharField(
        max_length=20,
        choices=[
            ("new", "New"),
            ("picked", "Picked"),
            ("delivered", "Delivered")
        ],
        default="new"
    )

    notified = models.BooleanField(default=False)  # 🔒 PREVENTS DUPLICATES

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.status}"

    def save(self, *args, **kwargs):
        if not self.token:
            # Generates a random 6-digit number like '482931'
            self.token = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a Profile when a User is created."""
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Ensure the Profile is saved when the User is saved."""
    # This prevents errors if a profile somehow wasn't created
    if hasattr(instance, 'profile'):
        instance.profile.save()