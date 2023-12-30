from .models import *

def footer_data(request):
    try:
        settings_instance = Settings.objects.get(status=True)
    except Settings.DoesNotExist:
        settings_instance = None
        
    return {'footer_data': settings_instance}

     
    