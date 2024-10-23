from django.shortcuts import render
from django.db.models import Q
from .models import CDBEntry

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

def index_view(request):
    context = get_cdb_entry_context(request)
    return render(request, 'cdb/index_view.html', context)