from django.db import models
from django.contrib.auth.models import User

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)
    food_name = models.CharField(max_length=200)
    food_price = models.DecimalField(max_digits=10, decimal_places=2)
    food_image = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        return self.food_price * self.quantity

    def __str__(self):
        return f"{self.food_name} - {self.quantity}"
