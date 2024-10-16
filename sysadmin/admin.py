from django.contrib import admin
from .models import Manager

class ManagerAdmin(admin.ModelAdmin):
    model = Manager
    filter_horizontal = ['subordinates']

admin.site.register(Manager)