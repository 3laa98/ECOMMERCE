from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.cache import patch_cache_control
from django.views.decorators.http import require_http_methods, require_POST

from store.filters import ProductFilter
from store.forms import ProductForm
from store.models import Product, Category

# Create your views here.


# @login_required
def store(request):
    new_products = Product.objects.all().order_by('-created_at')[:6]
    context = {'new_products': new_products}
    return render(request, 'store/store.html', context=context)


@login_required
def product_info(request, product_slug):
    # cache_key = f"product_{product_slug}"  # Unique key for each product
    # product = cache.get(cache_key)  # Try to get product from cache

    product = get_object_or_404(Product, slug=product_slug)

    # cache.set(cache_key, product, timeout=60 * 15)  # Store in cache for 15 minutes
    response = render(request, 'store/product_info.html', context={'product': product})
    # patch_cache_control(response, public=True, max_age=3600)
    return response


def product_list(request):
    products = Product.objects.all()  # Get all products

    # Initialize the filter with GET parameters from the request
    # product_filter = ProductFilter(request.GET, queryset=Product.objects.all().order_by('price'))

    # Get the filtered products and paginate them
    # products = product_filter.qs

    # Set up pagination (10 products per page)
    paginator = Paginator(products, 5)
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(
        page_number
    )  # Get the products for the requested page
    # context={'page_obj': page_obj, 'filter': product_filter}
    return render(request, 'store/product_list.html', {'page_obj': page_obj})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect('store')
        else:
            print(form.errors)
    else:
        form = ProductForm()

    context = {'form': form}
    return render(request, 'store/add_product.html', context=context)


@require_POST
def del_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('store')

def get_new_products(request):
    new_products = Product.objects.all().order_by('-created_at')[:6]

