import time
from django.http import HttpResponseBadRequest
from .models import SecurityLog
from .utils.telegram import send_telegram_alert


class CyberSecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        start_time = time.time()

        # ------------------------------------------------------------------
        # 1. PRE-READ CHECK (Prevents RequestDataTooBig Crash)
        # ------------------------------------------------------------------
        # We check the CONTENT_LENGTH header before touching request.body.
        # This allows us to log and alert BEFORE Django's internal limit kicks in.
        content_length = request.META.get('CONTENT_LENGTH')

        if content_length:
            try:
                data_size = int(content_length)
                # 1,000,000 bytes = ~1MB
                if data_size > 1000000:
                    # Log to Database immediately
                    SecurityLog.objects.create(
                        event_type='DATA_VOL',
                        ip_address=ip,
                        path=request.path,
                        details=f"Blocked payload attempt: {data_size} bytes.",
                        severity=2
                    )

                    # Send Telegram Alert
                    send_telegram_alert(
                        f"⚠️ *LARGE PAYLOAD BLOCKED*\n"
                        f"IP: `{ip}`\n"
                        f"Path: `{request.path}`\n"
                        f"Size: `{data_size}` bytes"
                    )

                    # Return response here so Django doesn't try to parse the body
                    return HttpResponseBadRequest("Payload too large. Security alert triggered.")
            except (ValueError, TypeError):
                pass

        # ------------------------------------------------------------------
        # 2. PROCEED TO VIEW
        # ------------------------------------------------------------------
        response = self.get_response(request)

        # ------------------------------------------------------------------
        # 3. POST-RESPONSE LOGGING
        # ------------------------------------------------------------------
        duration = time.time() - start_time

        # Log Critical Server Errors (500+)
        if response.status_code >= 500:
            SecurityLog.objects.create(
                event_type='BREAKAGE',
                ip_address=ip,
                path=request.path,
                details=f"Server Error {response.status_code}. Processing: {duration:.2f}s",
                severity=3
            )
            send_telegram_alert(
                f"🚨 *SERVER ERROR {response.status_code}*\n"
                f"IP: `{ip}`\n"
                f"Path: `{request.path}`\n"
                f"Processing Time: `{duration:.2f}s`"
            )

        return response

    # ------------------------------------------------------------------
    # 4. GLOBAL EXCEPTION CATCHER (The Safety Net)
    # ------------------------------------------------------------------
    def process_exception(self, request, exception):
        """
        Runs if a view crashes or if Django's internal settings kill the request.
        This captures the 'RequestDataTooBig' error if it happens elsewhere.
        """
        ip = request.META.get('REMOTE_ADDR')

        SecurityLog.objects.create(
            event_type='CRITICAL',
            ip_address=ip,
            path=request.path,
            details=f"Critical Exception: {str(exception)}",
            severity=3
        )

        send_telegram_alert(
            f"💀 *CRITICAL SYSTEM EXCEPTION*\n"
            f"IP: `{ip}`\n"
            f"Error: `{str(exception)}`"
        )

        return None  # Let Django handle the standard error display