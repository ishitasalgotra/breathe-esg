from django.contrib import admin
from .models import EmissionRecord, NormalizationRule

admin.site.register(EmissionRecord)
admin.site.register(NormalizationRule)


