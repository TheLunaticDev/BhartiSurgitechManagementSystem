from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import F
from .models import TPEntry
from crm.models import Entry
from cdb.models import CDBEntry

def tp_toggle_not_visited(request, entry_id):
    entry = get_object_or_404(TPEntry, id=entry_id)
    entry.not_visited = not entry.not_visited
    entry.save()
    
    context = {
        'entry': entry,
    }

    return render(request, 'tp/partials/_table_row.html', context)

def edit_field(request, entry_id, field_name):
    entry = get_object_or_404(TPEntry, id=entry_id)
    context = {
        'entry': entry,
        'field_name': field_name,
        'field_value': getattr(entry, field_name),
    }
    return render(request, 'tp/includes/edit_field.html', context)

def update_field(request, entry_id, field_name):
    if request.method == 'POST':
        entry = get_object_or_404(TPEntry, id=entry_id)
        new_value = request.POST.get('value')
        setattr(entry, field_name, new_value)
        entry.save()
        
        return JsonResponse({'new_value': new_value})

def tp_popover_content(request, entry_id):
    entry = get_object_or_404(TPEntry, id=entry_id)
    popover_edit_link = reverse('admin:tp_tpentry_change', args=(entry_id,))
    return render(request, 'tp/partials/_popover_content.html', {'entry': entry, 'popover_edit_link': popover_edit_link})

@login_required
def index_view(request):
    entries = TPEntry.objects.all().filter(owner=request.user).order_by(F('schedule').asc(nulls_last=True), F('stage__order').asc(nulls_last=True))
    context = {
        'entries': entries,
    }
    return render(request, 'tp/index_view.html', context)

@login_required
def edit_view(request):
    entries = TPEntry.objects.all().filter(owner=request.user).order_by(F('schedule').asc(nulls_last=True), F('stage__order').asc(nulls_last=True))
    context = {
        'entries': entries,
    }
    return render(request, 'tp/edit_view.html', context)

@login_required
def add_entry_from_crm(request):
    if request.method == 'POST':
        selected_checkboxes = request.POST.getlist('selected-checkboxes')
        
        for id in selected_checkboxes:
            entry = Entry.objects.get(id=int(id))
            new_tp_entry = TPEntry()
            new_tp_entry.owner = entry.owner
            new_tp_entry.institute = entry.institute
            new_tp_entry.area = entry.area
            new_tp_entry.landmark = entry.landmark
            new_tp_entry.sector = entry.sector
            new_tp_entry.discipline = entry.discipline
            new_tp_entry.hospital_type = entry.hospital_type
            new_tp_entry.stage = entry.stage
            new_tp_entry.type = new_tp_entry.CRM
            new_tp_entry.link = entry.id
            new_tp_entry.save()
            new_tp_entry.products.set(entry.products.all())
            new_tp_entry.save()
            entry.has_been_sent_to_tp = True
            entry.save()
        
        return redirect('tp_index_view')

    return redirect('crm_index_view')

@login_required
def add_entry_from_cdb(request):
    if request.method == 'POST':
        selected_checkboxes = request.POST.getlist('selected-checkboxes')
        
        for id in selected_checkboxes:
            entry = CDBEntry.objects.get(id=int(id))
            new_tp_entry = TPEntry()
            new_tp_entry.owner = request.user
            new_tp_entry.institute = entry.institute
            new_tp_entry.area = entry.area
            new_tp_entry.landmark = entry.landmark
            new_tp_entry.sector = entry.sector
            new_tp_entry.discipline = entry.discipline
            new_tp_entry.hospital_type = entry.hospital_type
            new_tp_entry.type = new_tp_entry.CDB
            new_tp_entry.link = entry.id
            new_tp_entry.save()
        
        return redirect('tp_index_view')

    return redirect('cdb_index_view')
