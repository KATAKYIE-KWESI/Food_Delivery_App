# Jolly/utils/sms.py
from sib_api_v3_sdk import ApiClient, Configuration
from sib_api_v3_sdk.api import transactional_sms_api
from sib_api_v3_sdk.models import SendTransacSms

import os

# You can store your API key in environment variable for safety
BREVO_API_KEY = os.environ.get("BREVO_API_KEY", "YOUR_BREVO_API_KEY")

def send_sms(to, message):
    """
    Sends an SMS via Brevo (Sendinblue).
    `to` should include country code, e.g., '233501234567'
    """
    configuration = Configuration()
    configuration.api_key['api-key'] = BREVO_API_KEY

    api_instance = transactional_sms_api.TransactionalSMSApi(ApiClient(configuration))

    sms = SendTransacSms(
        sender="JollyFoods",  # Can be alphanumeric (max 11 chars)
        recipient=to,
        content=message
    )

    try:
        response = api_instance.send_transac_sms(sms)
        print(f"✅ SMS sent to {to}. Message ID: {response['messageId']}")
    except Exception as e:
        print(f"❌ SMS sending failed to {to}. Error: {e}")
