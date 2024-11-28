from urllib.parse import urlparse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse, resolve
from django.db.models import Q
from django.db.models.functions import Lower
from .models import CDBEntry
from crm.models import State, District, Discipline, HospitalType, Sector

def cdb_add_state_filter(request):
    state = request.GET.get('add_state')
    state = get_object_or_404(State, id=state)


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
    filter_states = request.GET.getlist('filter_state')
    filter_districts = request.GET.getlist('filter_district')
    filter_disciplines = request.GET.getlist('filter_discipline')
    filter_hospital_types = request.GET.getlist('filter_hospital_type')
    filter_sectors = request.GET.getlist('filter_sector')
    filter_owners = request.GET.getlist('filter_owner')

    filter_conditions = Q()
    
    if filter_states:
        filter_conditions |= Q(area__district__state__id__in=filter_states)
    
    if filter_districts:
        filter_conditions |= Q(area__district__id__in=filter_districts)

    if filter_disciplines:
        filter_conditions |= Q(discipline__id__in=filter_disciplines)

    if filter_hospital_types:
        filter_conditions |= Q(hospital_type__id__in=filter_hospital_types)

    if filter_sectors:
        filter_conditions |= Q(sector__id__in=filter_sectors)

    if filter_owners:
        filter_conditions |= Q(owner__id__in=filter_owners)

    cdbentries = CDBEntry.objects.filter(filter_conditions).order_by('owner', 'area__district__state__name', 'area__district__name', 'area__name')

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
        'districts': District.objects.all().order_by(Lower('name')),
        'disciplines': Discipline.objects.all().order_by(Lower('name')),
        'hospital_types': HospitalType.objects.all().order_by(Lower('name')),
        'sectors': Sector.objects.all().order_by(Lower('name')),
        'owners': User.objects.all().order_by(Lower('first_name'), Lower('last_name'), Lower('username')),
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
    entries_per_page = 50
    page_number = request.GET.get('page', 1)
    
    entries = get_cdb_entries(request)
    paginator = Paginator(entries, entries_per_page)
    
    page_obj = paginator.get_page(page_number)

    print(request.GET)

    return render(request, "cdb/partials/select/cdbentry_list.html", {"page_obj": page_obj})

@login_required
def select_view(request):
    entries_per_page = 50
    page_number = request.GET.get('page', 1)

    entries = get_cdb_entries(request)
    paginator = Paginator(entries, entries_per_page)
    
    page_obj = paginator.get_page(page_number)

    submitted_form = get_submitted_form(request)

    context = {
        'page_obj': page_obj,
        'states': State.objects.all(),
        'districts': District.objects.all().order_by(Lower('name')),
        'disciplines': Discipline.objects.all().order_by(Lower('name')),
        'hospital_types': HospitalType.objects.all().order_by(Lower('name')),
        'sectors': Sector.objects.all().order_by(Lower('name')),
        'owners': User.objects.all().order_by(Lower('first_name'), Lower('last_name'), Lower('username')),
        'submitted_form': submitted_form,
    }

    return render(request, 'cdb/select_view.html', context)