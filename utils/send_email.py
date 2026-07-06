import resend
import os
from django.template.loader import render_to_string


resend.api_key = os.environ.get("RESEND_API_KEY")


def send_email(subject, to, context, template):

    html_message = render_to_string(template, context)
    params = {
        "from": "onboarding@resend.dev",  # بعداً دامین خودت را متصل کن
        "to": [to],
        "subject": subject,
        "html": html_message,
    }
    resend.Emails.send(params)