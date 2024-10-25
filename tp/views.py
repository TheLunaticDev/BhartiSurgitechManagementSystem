from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TPEntry
from crm.models import Entry

def tp_popover_content(request, entry_id):
    entry = get_object_or_404(TPEntry, id=entry_id)
    return render(request, 'crm/includes/_popover_content.html', {'entry': entry})


@login_required
def index_view(request):
    entries = TPEntry.objects.all().filter(owner=request.user)
    context = {
        'entries': entries,
    }
    return render(request, 'tp/index_view.html', context)

@login_required
def edit_view(request):
    entries = TPEntry.objects.all().filter(owner=request.user)
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
            new_tp_entry.save()
            new_tp_entry.products.set(entry.products.all())
            new_tp_entry.save()
        
        return redirect('tp_index_view')

    return redirect('crm_index_view')
