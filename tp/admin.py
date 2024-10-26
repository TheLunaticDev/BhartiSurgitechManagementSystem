from django.contrib import admin
from .models import TPEntry, PurposeType, Purpose


admin.site.register(PurposeType)
admin.site.register(Purpose)
admin.site.register(TPEntry)