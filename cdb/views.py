from urllib.parse import urlparse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse, resolve
from django.db.models import Q
from .models import CDBEntry
from crm.models import State, District

def get_submitted_form(request):
    form = {}

    if request.GET.get('add_state'):
        form['state'] = request.GET.get('add_state')

    if request.GET.get('add_district'):
        form['district'] = request.GET.get('add_district')

    return form


def cdb_toggle_visited(request, entry_id):
    if request.method == 'POST':
        entry = get_object_or_404(CDBEntry, id=entry_id)
        entry.visited = not entry.visited
        entry.save()
        popover_edit_link = reverse('admin:cdb_cdbentry_change', args=(entry_id,))

        context = {
            'entry': entry,
            'hide_popover_products': True,
            'popover_edit_link': popover_edit_link,
        }

        return render(request, 'cdb/partials/_update_institute.html', context)
    

def cdb_popover_content(request, entry_id):
    entry = get_object_or_404(CDBEntry, id=entry_id)
    popover_edit_link = reverse('admin:cdb_cdbentry_change', args=(entry_id,))

    context = {
        'entry': entry,
        'hide_popover_products': True,
        'popover_edit_link': popover_edit_link,
    }
    return render(request, 'cdb/partials/_popover_content.html', context)

def get_cdb_entries(request):
    cdbentries = CDBEntry.objects.all().order_by('owner', 'area__district__state__name', 'area__district__name', 'area__name')

    state = request.GET.get('add_state')
    district = request.GET.get('add_district')

    if state:
        cdbentries = cdbentries.filter(area__district__state__code=state)

    if district:
        cdbentries = cdbentries.filter(area__district=district)

    print(len(cdbentries))
    
    return cdbentries

@login_required
def index_view(request):
    entries_per_page = 50 
    page_number = request.GET.get('page', 1)
    
    entries = get_cdb_entries(request)
    paginator = Paginator(entries, entries_per_page)

    page_obj = paginator.get_page(page_number)

    submitted_form = get_submitted_form(request)


    context = {
        'page_obj': page_obj,
        'states': State.objects.all(),
        'districts': District.objects.all(),
        'submitted_form': submitted_form,
    }
    return render(request, 'cdb/index_view.html', context)

@login_required
def cdbentry_list(request):
    entries_per_page = 50
    page_number = request.GET.get('page', 1)
    
    entries = get_cdb_entries(request)
    paginator = Paginator(entries, entries_per_page)

    page_obj = paginator.get_page(page_number)

    print(request.GET)

    return render(request, "cdb/partials/cdbentry_list.html", {"page_obj": page_obj})

@login_required
def cdbentry_list_for_select_view(request):

    print("CDBEntry for Select View Triggered........................")
    entries_per_page = 50
    page_number = request.GET.get('page', 1)
    
    entries = get_cdb_entries(request)
    paginator = Paginator(entries, entries_per_page)
    
    page_obj = paginator.get_page(page_number)

    for entry in page_obj:
        print(entry)
    
    return render(request, "cdb/partials/select/cdbentry_list.html", {"page_obj": page_obj})

@login_required
def select_view(request):
    entries_per_page = 50
    page_number = request.GET.get('page', 1)

    entries = get_cdb_entries(request)
    paginator = Paginator(entries, entries_per_page)
    
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'states': State.objects.all(),
    }

    return render(request, 'cdb/select_view.html', context)