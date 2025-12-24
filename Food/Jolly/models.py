from django.db import models
from django.contrib.auth.models import User


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)
    food_name = models.CharField(max_length=200)
    food_price = models.DecimalField(max_digits=10, decimal_places=2)
    food_image = models.ImageField(upload_to='food_images/')
    quantity = models.IntegerField(default=1 )
    added_at = models.DateTimeField(auto_now_add=True)

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
