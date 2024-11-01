from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from .models import CDBEntry

def cdb_popover_content(request, entry_id):
    entry = get_object_or_404(CDBEntry, id=entry_id)
    popover_edit_link = reverse('admin:cdb_cdbentry_change', args=(entry_id,))

    context = {
        'entry': entry,
        'hide_popover_products': True,
        'popover_edit_link': popover_edit_link,
    }
    return render(request, 'crm/includes/_popover_content.html', context)

def get_cdb_entry_context(request):
    query = request.GET.get('q')
    area = request.GET.get('area')
    district = request.GET.get('district')
    state = request.GET.get('state')

    entries = CDBEntry.objects.all()
    
    if query:
        entries = entries.filter(
            Q(institute__icontains=query) |
            Q(area__name__icontains=query) |
            Q(doctors__name__icontains=query) |
            Q(doctors__speciality__icontains=query) |
            Q(doctors__designation__icontains=query) |
            Q(doctors__phone_number__icontains=query) |
            Q(admins__name__icontains=query) |
            Q(admins__designation__icontains=query) |
            Q(admins__email__icontains=query) |
            Q(admins__phone_number__icontains=query) |
            Q(references__name__icontains=query) |
            Q(references__email__icontains=query) |
            Q(references__phone_number__icontains=query)
        )

    if area:
        entries = entries.filter(area=area)

    if district:
        entries = entries.filter(district=district)

    if state:
        entries = entries.filter(state=state)

    return {
        'entries': entries,
    }

@login_required
def index_view(request):
    context = get_cdb_entry_context(request)
    return render(request, 'cdb/index_view.html', context)

@login_required
def edit_view(request):
    context = get_cdb_entry_context(request)
    return render(request, 'cdb/edit_view.html', context)

@login_required
def select_view(request):
    context = get_cdb_entry_context(request)
    return render(request, 'cdb/cdb_select_view.html', context)