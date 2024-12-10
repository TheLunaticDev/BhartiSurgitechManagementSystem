from datetime import datetime
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from crm.models import Entry, Area, Product
from crm.views import get_subordinates
from .models import DemoEntry


def demo_index_view(request):
    demo_entries = DemoEntry.objects.all().order_by('start_datetime')

    context = {
        'demo_entries': demo_entries,
    }

    return render(request, 'demo/index.html', context)

def demo_add_get_form(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    user = entry.owner
    subordinates = get_subordinates(request)

    if user not in subordinates:
        return render('/')

    products = entry.products.all()

    context = {
        'owner': user,
        'entry': entry,
        'products': products,
    }

    return render(request, 'demo/partials/_demo_add_get_form.html', context)

def demo_load_entry_list_for_user(request):
    user = request.GET.get('add-demo-owner')
    user = get_object_or_404(User, id=user)
    entries = Entry.objects.filter(owner=user)

    context = {
        'entries': entries,
    }

    return render(request, 'demo/partials/_demo_add_get_entry_list.html', context)

@login_required
def demo_add_new_entry(request):
    if request.method == "POST":
        owner = request.POST.get('owner')
        institute = request.POST.get('institute')
        area = request.POST.get('area')
        product = request.POST.get('product')
        start = request.POST.get('start')
        end = request.POST.get('end')

        new_demo_entry = DemoEntry.objects.create(
            user=get_object_or_404(User, id=owner),
            institute=institute,
            area=get_object_or_404(Area, id=area),
            product=get_object_or_404(Product, id=product),
            start_datetime=datetime.strptime(start, "%m/%d/%Y"),
            end_datetime=datetime.strptime(end, "%m/%d/%Y"),
        )

        new_demo_entry.save()
        
        return redirect('crm_index_view')
    return redirect('crm_index_view')