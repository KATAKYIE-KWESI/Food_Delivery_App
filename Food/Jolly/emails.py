# your_app/emails.py

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_welcome_email(user):

   # Sends a welcome email with a discount code to a newly registered user.

    # Context for the HTML template
    context = {
        'username': user.username,
        'discount_code': 'JOLLY20',  # The special welcome discount
        'app_name': 'JollyFoods'
    }

    # 1. Load the HTML template content
    # You must create this file: templates/welcome_email.html
    try:
        html_message = render_to_string('welcome_email.html', context)
        plain_message = strip_tags(html_message)  # Plain text fallback
    except Exception as e:
        # Fallback if template rendering fails
        print(f"Template rendering failed: {e}")
        plain_message = f"Welcome to JollyFoods, {user.username}! Use code JOLLY20 for 20% off your first order."
        html_message = None

    # 2. Define email metadata
    subject = '🎉 Welcome to JollyFoods! Your 20% Discount is Ready!'
    recipient_list = [user.email]

    # 3. Send the email
    try:
        # Use send_mail with html_message argument
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            html_message=html_message,  # Send the styled HTML version
            fail_silently=False,
        )
        print(f"SUCCESS: Welcome email sent to {user.email}")
    except Exception as e:
        print(f"FAILURE: Could not send welcome email to {user.email}. Error: {e}")