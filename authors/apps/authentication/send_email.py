
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
import os   


def send_email(recipient, token, request):
    subject = "Password Reset"
    sender = os.getenv('EMAIL_SENDER')
    host_url = get_current_site(request)
    content = 'You are receiving this email because we received a password \
    reset request for your account on'
    reset_link = "http://" + host_url.domain + \
        '/api/v1/users/password_update/'+token.decode()+' to reset your \
                                                    password'
    email_message = render_to_string('email_verification.html', {
        'content': content,
        'verification_link': reset_link,
        'title': subject,
        'message_action': ' to reset your password.'
    })
    email_content = strip_tags(email_message)
    msg = EmailMultiAlternatives(
        subject, email_content, sender, to=[recipient])
    msg.attach_alternative(email_message, "text/html")
    msg.send()
    result = {
        'message': 'A password reset link has been sent to your email'
    }
    return result
