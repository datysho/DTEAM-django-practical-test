import os
from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from weasyprint import HTML
from django.conf import settings
from .models import CV

@shared_task
def send_cv_pdf_email(cv_id, recipient_email):
    """
    Generate a PDF from the CV detail template and send it via email.
    """
    try:
        cv = CV.objects.get(pk=cv_id)
    except CV.DoesNotExist:
        return "CV not found"

    # Render HTML for the PDF using a dedicated template
    html_string = render_to_string("main/cv_detail_pdf.html", {"cv": cv})
    pdf = HTML(string=html_string, base_url=settings.BASE_DIR).write_pdf()

    subject = f"CV of {cv.firstname} {cv.lastname}"
    message = "Please find attached the PDF of the CV."
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])
    email.attach(f"cv_{cv_id}.pdf", pdf, "application/pdf")
    email.send()
    return "Email sent successfully"

