from django.core.mail import send_mail
from django.conf import settings


def send_email_without_delay(subject, html_message, email_list):
    send_mail(
        subject=subject,
        message=None,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email_list],
        html_message=html_message
    )
    return True