from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseInlineFormSet
from django.shortcuts import redirect
from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest
from django.http.response import HttpResponse
from .models import (
    Entry, Area, Stage, StageGroup,
    Category, Product, Doctor, Administrator,
    Reference, State, District, ProductEntry,
    Sector, Discipline, HospitalType, Configuration,
)
from .forms import AreaModelForm, DoctorInlineForm, CategoryForm, StageGroupForm
from sysadmin.models import Manager


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'products', 'text_color', 'order']
    form = CategoryForm

    def products(self, obj):
        return ", ".join([product.name for product in obj.products.all()])
    products.short_description = 'Products'


class StageGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'stages', 'text_color', 'order']
    form = StageGroupForm
    
    def stages(self, obj):
        return ", ".join([stage.name for stage in obj.stages.all()])
    stages.short_description = 'Stages'


class StageAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'win', 'order', 'group', 'tracks_for_tp']

    def tracks_for_tp(self, obj):
        return "Yes" if obj.tracks_tp_link else "No"

    tracks_for_tp.short_description = "Track for TP?"
    


class AdministratorAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'email', 'designation']

    
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'email', 'designation', 'speciality']

    
class SourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'email']


class StateAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']

    
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'state']


class AreaAdmin(admin.ModelAdmin):
    form = AreaModelForm


class ConfigurationInline(admin.TabularInline):
    model = Configuration
    verbose_name = 'Configurations'
    verbose_name_plural = 'Add Configurations here'
    extra = 1
    classes = ['collapse']

    
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category','quoted_price', 'cutoff', 'purchase_price', 'dealer_price', 'va_percentage', 'gross_va', 'net_va', 'incentive']
    list_filter = ['category']
    inlines = [ConfigurationInline]


class AdministratorInline(admin.TabularInline):
    model = Administrator
    verbose_name = 'Administrator'
    verbose_name_plural = 'Add Admins here'
    extra = 1
    classes = ['collapse']


class DoctorInline(admin.TabularInline):
    model = Doctor
    extra = 3
    verbose_name = 'Doctor'
    verbose_name_plural = 'Add Doctors here'
    classes = ['collapse']

    
class ReferenceInline(admin.TabularInline):
    model = Reference
    extra = 1
    verbose_name = 'Reference'
    verbose_name_plural = 'Add Reference here'
    classes = ['collapse']


class ProductEntryAdmin(admin.ModelAdmin):
    list_display = ['product', 'entry', 'count']

class ProductEntryInline(admin.TabularInline):
    model = ProductEntry
    extra = 1
    fields = ['product', 'count']
    classes = ['collapse']
   

class EntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'institute', 'time_since_creation', 'owner']

    fieldsets = [
        ('Entry Information', {'fields': [('institute', 'area', 'stage'), ('expected', 'notes'), ('landmark', 'hospital_type', 'sector', 'discipline')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['created_on', 'owner']
    inlines = [ProductEntryInline, AdministratorInline, DoctorInline, ReferenceInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Manager').exists():
            if Manager.objects.filter(user=request.user).exists():
                manager = Manager.objects.get(user=request.user)
                subordinates = manager.subordinates.all()
                subordinate_ids = subordinates.values_list('id', flat=True)
                return qs.filter(owner__in=subordinate_ids)
        if request.user.groups.filter(name='Employee').exists():
            return qs.filter(owner=request.user)
        return qs

    def save_model(self, request, obj,  form, change):
        if not obj.pk:
            obj.owner = request.user
        super().save_model(request, obj, form, change)
    
    def response_add(self, request, obj):
        return redirect('/')

admin.site.register(Entry, EntryAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(StageGroup, StageGroupAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Administrator, AdministratorAdmin)
admin.site.register(Reference, SourceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(ProductEntry, ProductEntryAdmin)
admin.site.register(Sector)
admin.site.register(Discipline)
admin.site.register(HospitalType)