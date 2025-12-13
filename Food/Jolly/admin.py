from django.contrib import admin
from django.contrib import admin
from .models import CartItem

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        'food_name',
        'food_price',
        'quantity',
        'get_total_price',
        'user',
        'session_key',
        'added_at',
    )

    list_filter = ('added_at',)
    search_fields = ('food_name', 'user__username', 'session_key')

