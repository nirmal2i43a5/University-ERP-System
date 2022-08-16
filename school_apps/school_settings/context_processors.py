from django.shortcuts import get_object_or_404
from .models import MisSetting

def settings_detail(request):
    detail = get_object_or_404(MisSetting,id = 1)
    # current_datetime = datetime.datetime.now()
    return {'setting_instance':detail, 
            # 'current_year': current_datetime.year
            }
