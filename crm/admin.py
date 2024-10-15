from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseInlineFormSet
from django.shortcuts import redirect
from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest
from django.http.response import HttpResponse
from .models import (
    Entry, Area, Stage,
    Category, Product, Doctor, Administrator,
    Reference, State, District,
)
from .forms import AreaModelForm, DoctorInlineForm
from sysadmin.models import Manager


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'products']

    def products(self, obj):
        return ", ".join([product.name for product in obj.products.all()])
    products.short_description = 'Products'

class StageAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'win']


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

    
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']

    
class ProductInline(admin.TabularInline):
    model = Entry.products.through
    verbose_name = 'Product'
    verbose_name_plural = 'Select Products Here'
    extra = 1
    classes = ['collapse']

    
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
   

class EntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'institute', 'time_since_creation', 'owner']

    fieldsets = [
        ('Entry Information', {'fields': [('institute', 'area', 'stage'), ('expected', 'va', 'notes', 'schedule_date')], 'classes': ['collapse']}),
        ('Products', {'fields': ['products'], 'classes': ['collapse']}),
    ]
    filter_horizontal = ['products']
    readonly_fields = ['created_on', 'owner']
    inlines = [AdministratorInline, DoctorInline, ReferenceInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Manager').exists():
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
    
    def response_add(self, request, obj, post_url_continue=None):
        if request.user.groups.filter(name='Employee').exists():
            return redirect('/')
        else:
            return HttpResponse('You are not an employee, you cannot add an entry')

    def response_change(self, request, obj, post_url_continue=None):
        if request.user.groups.filter(name='Manager').exists():
            referer_url = request.session['last_manager_edit_link']
            if referer_url:
                return redirect(referer_url)
            else:
                return redirect('crm_manager_edit_view')
        elif request.user.groups.filter(name='Employee').exists():
            return redirect('/edit/')

        else:
            return redirect('/')


admin.site.register(Entry, EntryAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Administrator, AdministratorAdmin)
admin.site.register(Reference, SourceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(State, StateAdmin)