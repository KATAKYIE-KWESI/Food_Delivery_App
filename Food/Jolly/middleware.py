from .models import SecurityLog
from .utils.telegram import send_telegram_alert
import time

class CyberSecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        start_time = time.time()

        # Track Data Usage (Incoming Payload)
        data_size = len(request.body) if request.body else 0

        response = self.get_response(request)

        duration = time.time() - start_time

        # 1. LOG CRITICAL BREAKAGES (Status 500)
        if response.status_code >= 500:
            SecurityLog.objects.create(
                event_type='BREAKAGE',
                ip_address=ip,
                path=request.path,
                details=f"Server Error 500. Processing time: {duration}s",
                severity=3
            )
            send_telegram_alert(f"🚨 Server Error 500 detected from IP {ip} at {request.path}")

        # 2. LOG SUSPICIOUS DATA USAGE (payloads > 1MB)
        if data_size > 1000000:
            SecurityLog.objects.create(
                event_type='DATA_VOL',
                ip_address=ip,
                path=request.path,
                details=f"Large payload detected: {data_size} bytes.",
                severity=2
            )
            send_telegram_alert(f"⚠️ Large payload ({data_size} bytes) detected from IP {ip} at {request.path}")

        return response
