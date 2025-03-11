from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from .models import CV, RequestLog
from .tasks import send_cv_pdf_email
from django.conf import settings
from openai import OpenAI


def cv_pdf(request, id):
    """
    Generate a PDF version of the CV detail.
    """
    cv = get_object_or_404(CV, id=id)
    # Render a template to a HTML string specifically for PDF
    html_string = render_to_string('main/cv_detail_pdf.html', {'cv': cv})
    # Use request.build_absolute_uri() as the base URL for relative assets
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="cv_{}.pdf"'.format(cv.id)
    return response


def cv_list(request):
    cvs = CV.objects.all()
    return render(request, 'main/cv_list.html', {'cvs': cvs})


def cv_detail(request, id):
    cv = get_object_or_404(CV, id=id)
    return render(request, 'main/cv_detail.html', {'cv': cv})


def recent_logs(request):
    logs = RequestLog.objects.all().order_by('-timestamp')[:10]
    return render(request, 'main/recent_logs.html', {'logs': logs})


def settings_page(request):
    """
    Render a settings page displaying selected Django settings.
    """
    return render(request, 'main/settings.html')

def send_pdf_email(request, id):
    if request.method == "POST":
        recipient_email = request.POST.get("email")
        # Optionally, validate the email
        cv = get_object_or_404(CV, pk=id)
        # Trigger the Celery task asynchronously.
        send_cv_pdf_email.delay(id, recipient_email)
        # Redirect back to the CV detail page (you can add a success message if desired)
        return redirect("cv_detail", id=id)
    return redirect("cv_detail", id=id)

def translate_cv(request, id):
    cv = get_object_or_404(CV, id=id)
    if request.method == "POST":
        target_language = request.POST.get("language")
        # Combine CV content; adjust as needed for your use case.
        text_to_translate = (
            f"Name: {cv.firstname} {cv.lastname}\n"
            f"Skills: {cv.skills}\n"
            f"Projects: {cv.projects}\n"
            f"Bio: {cv.bio}\n"
            f"Contacts: {cv.contacts}"
        )
        translated_text = translate_text_with_openai(text_to_translate, target_language)
        return render(request, "main/cv_translated.html", {
            "cv": cv,
            "translated_text": translated_text,
            "target_language": target_language,
        })
    return redirect("cv_detail", id=id)


def translate_text_with_openai(text, target_language):
    """
    Uses the new OpenAI Python API (v1) to translate text into the target language.
    """
    # Create a client instance using the API key from settings
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    prompt = f"Translate the following text into {target_language}:\n\n{text}"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a translation assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )
    
    # Access the translated text using the new attribute syntax
    translated_text = response.choices[0].message.content.strip()
    return translated_text
