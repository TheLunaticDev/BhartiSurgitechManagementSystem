from django.contrib import admin
from .models import (
    CDBAdministrator, CDBDoctor,
    CDBReference, CDBEntry,
)


class CDBAdministratorInline(admin.TabularInline):
    model = CDBAdministrator
    verbose_name = 'Administrator'
    verbose_name_plural = 'Add Admins here'
    extra = 1
    classes = ['collapse']

    
class CDBDoctorInline(admin.TabularInline):
    model = CDBDoctor
    verbose_name = 'Doctor'
    verbose_name_plural = 'Add Doctors here'
    extra = 1
    classes = ['collapse']

    
class CDBReferenceInline(admin.TabularInline):
    model = CDBReference
    verbose_name = 'Reference'
    verbose_name_plural = 'Add References here'
    extra = 1
    classes = ['collapse']

    
class CDBEntryAdmin(admin.ModelAdmin):
    list_display = ['institute', 'location', 'discipline', 'hospital_type', 'sector', 'owner__first_name']
    fieldsets = [
        ('Entry Information', {'fields': [('owner', 'institute'), ('area', 'landmark'), ('sector', 'discipline', 'hospital_type')], 'classes': ['collapse']}),
    ]
    inlines = [CDBAdministratorInline, CDBDoctorInline, CDBReferenceInline]
    list_filter = ['area', 'sector', 'discipline', 'hospital_type', 'area__district__name', 'area__district__state__name', 'owner']


admin.site.register(CDBEntry, CDBEntryAdmin)