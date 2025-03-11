from django.conf import settings

def settings_context(request):
    """
    Injects the Django settings into the template context.
    """
    return {'settings': settings}

