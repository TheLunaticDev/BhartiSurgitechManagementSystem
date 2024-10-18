from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.urls import reverse
from django.db.models import Q, Prefetch
from .models import (
    Area, Entry, Stage, District, Doctor, State, Product,
)
from .decorators import group_required
from sysadmin.models import Manager
from dal import autocomplete

def get_manager_entry_context(request, subordinate_id):
    query = request.GET.get('q')
    expected = request.GET.get('expected')
    va = request.GET.get('va')
    stage = request.GET.get('stage')
    area = request.GET.get('area')
    district = request.GET.get('district')
    state = request.GET.get('state')
    product = request.GET.get('product')

    try:
        manager = Manager.objects.get(user=request.user)
    except Manager.DoesNotExist:
        manager = None
        
    if manager is None:
        return {
            'stages': Stage.objects.all(),
            'states': State.objects.all(),
            'subordinate_id': subordinate_id if subordinate_id is not None else '',
        }

    # Retrieve subordinates under the manager
    subordinates = manager.subordinates.all()

    # Include manager's own entries and subordinate entries
    if subordinate_id:
        # Filter entries belonging to a specific subordinate
        entries = Entry.objects.filter(owner=get_object_or_404(User, id=subordinate_id))
    else:
        # Include both the manager's own entries and subordinate entries
        entries = Entry.objects.filter(Q(owner=request.user) | Q(owner__in=subordinates))

    # Apply search query if provided
    if query:
        entries = entries.filter(
            Q(institute__icontains=query) |
            Q(area__name__icontains=query) |
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
            Q(references__email__icontains=query) |
            Q(references__phone_number__icontains=query) |
            Q(notes__icontains=query)
        )
    
    if expected:
        entries = entries.filter(expected=expected)
    
    if va:
        entries = entries.filter(va=va)
    
    if stage:
        entries = entries.filter(stage=stage)
    
    if area:
        entries = entries.filter(area=area)

    if district:
        entries = entries.filter(area__district=district)
    
    if state:
        entries = entries.filter(area__district__state=state)
    
    if product:
        entries = entries.filter(products=product)
    
    entries = entries.prefetch_related(
        Prefetch(
            'products',
            queryset=Product.objects.select_related('category').order_by('category__order', 'name')
        )
    )

    # Add products information to entries
    entries_with_products = []
    for entry in entries:
        product_keys = [product.name for product in entry.products.all()]
        entry.available_products = "  |  ".join(product_keys)
        entries_with_products.append(entry)

    return {
        'entries': entries_with_products,
        'subordinates': subordinates,
        'stages': Stage.objects.all(),
        'states': State.objects.all(),
        'districts': District.objects.all(),
        'products': Product.objects.all(),
        'areas': Area.objects.all(),
        'subordinate_id': subordinate_id if subordinate_id is not None else '',
    }

def get_entry_context(request):
    query = request.GET.get('q')
    expected = request.GET.get('expected')
    va = request.GET.get('va')
    stage = request.GET.get('stage')
    area = request.GET.get('area')
    district = request.GET.get('district')
    state = request.GET.get('state')
    product = request.GET.get('product')

    entries = Entry.objects.filter(owner=request.user)

    if query:
        entries = entries.filter(
            Q(institute__icontains=query) |
            Q(area__name__icontains=query) |
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
            Q(references__email__icontains=query) |
            Q(references__phone_number__icontains=query) |
            Q(notes__icontains=query)
        ).filter(owner=request.user)
    
    if expected:
        entries = entries.filter(expected=expected)
    
    if va:
        entries = entries.filter(va=va)

    if stage:
        entries = entries.filter(stage=stage)
    
    if area:
        entries = entries.filter(area=area)

    if district:
        entries = entries.filter(area__district=district)
    
    if state:
        entries = entries.filter(area__district__state=state)

    if product:
        entries = entries.filter(products=product)
    
    entries = entries.prefetch_related(
        Prefetch(
            'products',
            queryset=Product.objects.select_related('category').order_by('category__order', 'name')
        )
    )

    entries_with_products = []

    for entry in entries:
        product_keys = []

        for product in entry.products.all():
            product_keys.append(product.name)

        entry.available_products = "  |  ".join(product_keys)

        entries_with_products.append(entry)
    
    return {
        'entries': entries_with_products,
        'stages': Stage.objects.all(),
        'states': State.objects.all(),
        'districts': District.objects.all(),
        'products': Product.objects.all(),
        'areas': Area.objects.all(),
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
    if subordinate_id is None:
        return render(request, 'crm/manager_index.html', context)
    else:
        return render(request, 'crm/manager_index_for_subordinate.html', context)

@login_required
def manager_edit_view(request, subordinate_id=None):
    context = get_manager_entry_context(request, subordinate_id)
    if subordinate_id is None:
        request.session['last_manager_edit_link'] = reverse('crm_manager_edit_view')
        return render(request, 'crm/manager_edit.html', context)
    else:
        request.session['last_manager_edit_link'] = reverse('crm_manager_edit_view_with_id', kwargs={'subordinate_id': subordinate_id})
        return render(request, 'crm/manager_edit_for_subordinate.html', context)

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