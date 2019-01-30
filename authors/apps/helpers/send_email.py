from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string

def send_email(email_subject, sender, recipient, email_data):
    email_message = render_to_string('email_template.html', {
            'message_content': email_data[0],
            'button_content': email_data[1],
            'verification_link': email_data[2],
            'title': email_subject,
            'username': email_data[3],
            'article_title':email_data[4],
            'message_body':email_data[5]
        })
    email_content = strip_tags(email_message)
    msg = EmailMultiAlternatives(
        email_subject, email_content, sender, to=[recipient])
    msg.attach_alternative(email_message, "text/html")
    msg.send()
