import requests
from django.conf import settings

def send_telegram_alert(message: str):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print("Failed to send Telegram alert:", e)
