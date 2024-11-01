from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from crm.models import Product, Category

@login_required
def index_view(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }
    
    return render(request, 'productlist/index.html', context)

@login_required
def filter_by_category(request, category_id):
    if category_id == -1:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category=category_id)

    context = {
        'products': products,
    }

    return render(request, 'productlist/partials/table_body.html', context)

@login_required
def product_list_search(request):
    query = request.GET.get('query')
    if query is None:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(name__icontains=query)

    context = {
        'products': products,
    }

    return render(request, 'productlist/partials/table_body.html', context)

@login_required
def get_product_configurations(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    context = {
        'product': product,
    }

    return render(request, 'productlist/partials/product_configs.html', context)