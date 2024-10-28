from django.contrib import admin
from .models import TPEntry, PurposeType, Purpose

class TPEntryAdmin(admin.ModelAdmin):
    list_display = ['institute', 'location', 'stage__name', 'product_list', 'schedule', 'purpose', 'owner__first_name']


admin.site.register(PurposeType)
admin.site.register(Purpose)
admin.site.register(TPEntry, TPEntryAdmin)