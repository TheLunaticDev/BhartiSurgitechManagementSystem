from django.contrib import admin
from .models import Brochure, Setting


class SettingAdmin(admin.ModelAdmin):
    model = Setting
    list_display = ['key', 'description', 'value']

admin.site.register(Brochure)
admin.site.register(Setting, SettingAdmin)