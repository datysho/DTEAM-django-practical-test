from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from .models import CV, RequestLog


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

