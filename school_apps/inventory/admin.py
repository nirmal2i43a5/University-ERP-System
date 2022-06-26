from django.contrib import admin
from .models import StatusOptions, ProcurementRequest

# Register your models here.

admin.site.register(StatusOptions)
admin.site.register(ProcurementRequest)