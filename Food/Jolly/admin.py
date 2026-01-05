import psutil
import time
from django.contrib import admin
from django.db import connection
from django.db.models import Count  # <-- New Import
from .models import SecurityLog, CartItem


# --- Cart Item Admin ---
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('food_name', 'food_price', 'quantity','lat', 'lon', 'get_total_price', 'user', 'session_key', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('food_name', 'user__username', 'session_key')


# --- Security Log Admin (The SOC Dashboard) ---
@admin.register(SecurityLog)
class SecurityLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'event_type', 'ip_address', 'path', 'severity')
    list_filter = ('event_type', 'severity')
    readonly_fields = ('timestamp', 'ip_address', 'user_agent', 'path', 'details')

    def changelist_view(self, request, extra_context=None):
        # 1. Calculate live DB latency
        start = time.time()
        connection.ensure_connection()
        latency = (time.time() - start) * 1000

        # 2. Get data for the Pie Chart (Counting events)
        # This groups the logs by type and counts them
        chart_data = list(
            SecurityLog.objects.values('event_type')
            .annotate(total=Count('id'))
            .order_by('-total')
        )

        # 3. Combine everything into the dashboard context
        extra_context = extra_context or {}
        extra_context['chart_data'] = chart_data
        extra_context['system_health'] = {
            'cpu': psutil.cpu_percent(),
            'ram': psutil.virtual_memory().percent,
            'db_latency': f"{latency:.2f}ms",
            'active_logs': SecurityLog.objects.count()
        }

        return super().changelist_view(request, extra_context=extra_context)


from django.contrib import admin
from .models import Driver, Delivery

# Make Driver editable in admin
@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('user',)

# Make Delivery editable in admin
@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'driver', 'status', 'created_at')
    list_filter = ('status', 'driver')
