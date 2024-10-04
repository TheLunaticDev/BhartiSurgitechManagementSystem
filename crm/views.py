from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.urls import reverse
from django.db.models import Q
from .models import (
    Entry, Stage, District, Doctor, State
)
from .decorators import group_required
from sysadmin.models import Manager
from dal import autocomplete

def get_manager_entry_context(request, subordinate_id):
    query = request.GET.get('q')
    manager = Manager.objects.all().get(user=request.user)
    if manager is None:
        return
    subordinates = manager.subordinates.all()
    if query:
        if not subordinate_id:
            entries = Entry.objects.all().filter(
                Q(institute__icontains=query) |
                Q(area__name__icontains=query) |
                Q(area__district__name__icontains=query) |
                Q(area__district__state__name__icontains=query) |
                Q(stage__description__icontains=query) |
                Q(stage__name__icontains=query) |
                Q(stage__win__icontains=query) |
                Q(expected__icontains=query) |
                Q(va__icontains=query) |
                Q(products__name__icontains=query) |
                Q(products__category__name__icontains=query) |
                Q(doctors__name__icontains=query) |
                Q(doctors__speciality__icontains=query) |
                Q(doctors__designation__icontains=query) |
                Q(doctors__email__icontains=query) |
                Q(doctors__phone_number__icontains=query) |
                Q(admins__name__icontains=query) |
                Q(admins__designation__icontains=query) |
                Q(admins__email__icontains=query) |
                Q(admins__phone_number__icontains=query) |
                Q(references__name__icontains=query) |
                Q(references__email=query) |
                Q(references__phone_number=query) |
                Q(notes__icontains=query) |
                Q(created_on__icontains=query)
            ).filter(owner__in=subordinates)
        else:
            entries = Entry.objects.all().filter(
                Q(institute__icontains=query) |
                Q(area__name__icontains=query) |
                Q(area__district__name__icontains=query) |
                Q(area__district__state__name__icontains=query) |
                Q(stage__description__icontains=query) |
                Q(stage__name__icontains=query) |
                Q(stage__win__icontains=query) |
                Q(expected__icontains=query) |
                Q(va__icontains=query) |
                Q(products__name__icontains=query) |
                Q(products__category__name__icontains=query) |
                Q(doctors__name__icontains=query) |
                Q(doctors__speciality__icontains=query) |
                Q(doctors__designation__icontains=query) |
                Q(doctors__email__icontains=query) |
                Q(doctors__phone_number__icontains=query) |
                Q(admins__name__icontains=query) |
                Q(admins__designation__icontains=query) |
                Q(admins__email__icontains=query) |
                Q(admins__phone_number__icontains=query) |
                Q(references__name__icontains=query) |
                Q(references__email=query) |
                Q(references__phone_number=query) |
                Q(notes__icontains=query) |
                Q(created_on__icontains=query)
            ).filter(owner=User.objects.all().get(id=subordinate_id))
    else:
        if not subordinate_id:
            entries = Entry.objects.all().filter(owner__in=subordinates)
        else:
            entries = Entry.objects.all().filter(owner=User.objects.all().get(id=subordinate_id))

    entries_with_products = []

    for entry in entries:
        product_keys = []

        for product in entry.products.all():
            product_keys.append(product.name)

        entry.available_products = "  |  ".join(product_keys)

        entries_with_products.append(entry)

    return {
        'entries': entries_with_products,
        'subordinates': subordinates,
        'stages': Stage.objects.all(),
        'state': State.objects.all(),
    }


def get_entry_context(request):
    query = request.GET.get('q')
    if query:
        entries = Entry.objects.all().filter(
            Q(institute__icontains=query) |
            Q(area__name__icontains=query) |
            Q(area__district__name__icontains=query) |
            Q(area__district__state__name__icontains=query) |
            Q(stage__description__icontains=query) |
            Q(stage__name__icontains=query) |
            Q(stage__win__icontains=query) |
            Q(expected__icontains=query) |
            Q(va__icontains=query) |
            Q(products__name__icontains=query) |
            Q(products__category__name__icontains=query) |
            Q(doctors__name__icontains=query) |
            Q(doctors__speciality__icontains=query) |
            Q(doctors__designation__icontains=query) |
            Q(doctors__email__icontains=query) |
            Q(doctors__phone_number__icontains=query) |
            Q(admins__name__icontains=query) |
            Q(admins__designation__icontains=query) |
            Q(admins__email__icontains=query) |
            Q(admins__phone_number__icontains=query) |
            Q(references__name__icontains=query) |
            Q(references__email=query) |
            Q(references__phone_number=query) |
            Q(notes__icontains=query) |
            Q(created_on__icontains=query)
        ).filter(owner=request.user)
    else:
        entries = Entry.objects.all().filter(owner=request.user)

    entries_with_products = []

    for entry in entries:
        product_keys = []

        for product in entry.products.all():
            product_keys.append(product.name)

        entry.available_products = "  |  ".join(product_keys)

        entries_with_products.append(entry)
    
    return {
        'entries': entries_with_products,
    }

@login_required
def index_view(request):
    context = get_entry_context(request)
    return render(request, 'crm/index.html', context)

@login_required
def edit_view(request):
    context = get_entry_context(request)
    return render(request, 'crm/edit.html', context)

@login_required
def manager_index_view(request, subordinate_id=None):
    context = get_manager_entry_context(request, subordinate_id)
    return render(request, 'crm/manager_index.html', context)

@login_required
def manager_edit_view(request, subordinate_id=None):
    context = get_manager_entry_context(request, subordinate_id)
    request.session['last_manager_edit_link'] = reverse('crm_manager_edit_view', kwargs={'subordinate_id': subordinate_id})
    return render(request, 'crm/manager_edit.html', context)

class DistrictAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = District.objects.all()
        
        state_id = self.forwarded.get('state', None)
        if state_id:
            qs = qs.filter(state_id=state_id)
        
        return qs


class DoctorAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Doctor.objects.all()
        
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        
        return qs